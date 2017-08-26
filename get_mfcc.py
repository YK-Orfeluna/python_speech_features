# coding utf-8

"""
	https://github.com/jameslyons/python_speech_features
	↑を利用中
	
	$1: pcmlist

	pcmlistから，読むこむpcmファイルを判断
	pcmファイルの冒頭[0.5, 1, 2, 3, 4, 5, 10]秒を無発話区間として
	それぞれのMFCCとそのデルタを特徴量として取得する
	感覚は20ms, 10msごとに移動
	特徴量はその平均で，どちらも12次元
	結果は，それぞれ冒頭無発話区間ごとに，pcmファイル名と一緒にTSV形式で出力される
	出力は，このスクリプトと同階層のディレクトリ

"""

import wave
from time import ctime
import numpy as np
from python_speech_features import mfcc, delta, logfbank

def read_wav(wavname) :								# wavファイルを読み込んで，フレームレートと信号を出力
	with wave.open(wavname, "rb") as wf :
		rate = wf.getframerate()
		data = wf.readframes(rate)
		data = np.frombuffer(data, dtype=np.int16)
	return rate, data

def read_pcm(pcmname) :								# pcmファイルを読み込んで，信号を出力
	with open(pcmname, "rb") :
		data = pcm.read()
		data = np.frombuffer(data, np.int16)
	return data

def run(sec) :
	n = rate * sec

	for x, pcmname in enumerate(pcmnames) :
			data = read_pcm(pcmname)				# pcmファイルを読み込み
			data = data[: n]						# secに合わせて，冒頭区間のみを残す

			print("[%s]\nstart: open %s" %(ctime(), pcmname))


			# MFCCの計算とその平均
			mfcc_feature = mfcc(data, rate, winlen=length, winstep=step, numcep=n_feature)
			mfcc_mean = np.mean(mfcc_feature.T, axis=1).astype(np.str)

			#MFCCからデルタとその平均を求める
			d_mfcc_feat = delta(mfcc_feature, 2)
			d_mfcc_mean = np.mean(d_mfcc_feat.T, axis=1).astype(np.str)
			#print(d_mfcc_mean)

			# 結果（pcmファイル名，MFCC，デルタ）をまとめる
			rslt = np.array([pcmname], dtype=np.str)
			rslt = np.append(rslt, mfcc_mean)
			rslt = np.append(rslt, d_mfcc_mean)

			# 結果を1つの大きな配列に結合する
			if x == 0 :
				out = np.array([rslt])
			else :
				out = np.append(out, np.array([out]), axis=0)

			print("[%s]\ndone: get features from %s" %(ctime(), pcmname))

		# 全てのpcmファイルを読み込んだら，tsv形式で出力する
		ms = sec * 1000
		outname = "mfcc_feature_%sms.tsv" %ms
		np.savetxt(outname, out, delimiter="\t", fmt="%s")


if __name__ == "__main__" :
	from sys import argv
	from multiprocessing import Pool, cpu_count

	if len(argv) != 2 :
		exit("Error: missing args\narg: [pcm-list]")

	#wavname = "english.wav"
	#rate, data = read_wav(wavname)

	pcmlist = argv[1]
	#sec = float(argv[2])
	sec = (0.5, 1, 2, 3, 4, 5, 10)

	with open(pcmlist, "r") as fd :
		pcmnames = fd.read().strip().split("\n")
	pcmnames.sort()

	rate = 16000			# pcmファイルのフレームレート

	length = 20				# MFCCを計算する区間（ミリsec.）
	length /= 1000.0		# ミリsec.からsec.に変換

	step = 10				# MFCCを計算する区間の移動幅（ミリsec.）
	step /= 1000.0			# ミリsec.からsec.に変換

	n_feature = 12			# MFCCとデルタの次元数

	njobs = len(sec)		# njobsを決める（万が一，nCPUを超えたら調整）
	if njobs > cpu_count() :
		njobs = cpu_count()

	for s in sec :			# 回して回せば回す時
		p = Pool(njobs)
		p.map(run, s)

	exit("done: process")
