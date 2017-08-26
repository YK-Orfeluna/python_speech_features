# coding utf-8

import wave
from time import ctime
import numpy as np
from python_speech_features import mfcc, delta, logfbank

def read_wav(wavname) :
	with wave.open(wavname, "rb") as wf :
		rate = wf.getframerate()
		data = wf.readframes(rate)
		data = np.frombuffer(data, dtype=np.int16)
	return rate, data

def read_pcm(pcmname) :
	with open(pcmname, "rb") :
		data = pcm.read()
		data = np.frombuffer(data, np.int16)
	return data

if __name__ == "__main__" :
	from sys import argv

	#wavname = "english.wav"
	#rate, data = read_wav(wavname)

	pcmlist = argv[1]
	sec = float(argv[2])

	with open(pcmlist, "r") as fd :
		pcmnames = fd.read().strip().split("\n")
	pcmnames.sort()

	rate = 16000

	length = 20
	length /= 1000.0

	step = 10
	step /= 1000.0

	n_feature = 12

	for x, pcmname in enumerate(pcmnames) :
		data = read_pcm(pcmname)

		n = rate * sec
		data = data[: n]

		print("[%s]\nstart: open %s" %(ctime(), pcmname))

		mfcc_feature = mfcc(data, rate, winlen=length, winstep=step, numcep=n_feature)
		mfcc_mean = np.mean(mfcc_feature.T, axis=1).astype(np.str)

		d_mfcc_feat = delta(mfcc_feature, 2)
		d_mfcc_mean = np.mean(d_mfcc_feat.T, axis=1).astype(np.str)
		#print(d_mfcc_mean)

		#fbank_feat = logfbank(data, rate, winlen=length, winstep=step)
		#print(fbank_feat)

		rslt = np.array([pcmname], dtype=np.str)
		rslt = np.append(rslt, mfcc_mean)
		rslt = np.append(rslt, d_mfcc_mean)

		if x == 0 :
			out = np.array([rslt])
		else :
			out = np.append(out, np.array([out]), axis=0)

		print("[%s]\ndone: get features from %s" %(ctime(), pcmname))

	outname = "mfcc_feature.tsv"
	np.savetxt(outname, out, delimiter="\t", fmt="%s")

	exit("done: process")
