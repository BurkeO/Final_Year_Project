//import com.jlibrosa.audio.process.AudioFeatureExtraction;
//import com.jlibrosa.audio.wavFile.WavFile;
//
//import java.io.File;
//import java.math.RoundingMode;
//import java.text.DecimalFormat;
//
//public class JlibrosaMFCC
//{
//    int mNumFrames;
//    int mSampleRate;
//    int mChannels;
//
//    File sourceFile = new File("D:/Users/Owen/Final_Year_Project/birdsong/Common_Wood_Pigeon/Common_Wood_Pigeon_0.wav");
//
//    WavFile wavFile = WavFile.openWavFile(sourceFile);
//    mNumFrames = (int) wavFile.getNumFrames();
//    mSampleRate = (int) wavFile.getSampleRate();
//    mChannels = wavFile.getNumChannels();
//
//    float[][] buffer = new float[mChannels][mNumFrames];
//    int frameOffset = 0;
//    int loopCounter = ((mNumFrames * mChannels)/4096) + 1;
//        for (int i = 0; i < loopCounter; i++) {
//    frameOffset = wavFile.readFrames(buffer, mNumFrames, frameOffset);
//}
//
//
//    DecimalFormat df = new DecimalFormat("#.#####");
//        df.setRoundingMode(RoundingMode.CEILING);
//
//    float [] meanBuffer = new float[mNumFrames];
//        for(int q=0;q<mNumFrames;q++){
//    double frameVal = 0;
//    for(int p=0;p<mChannels;p++){
//        frameVal = frameVal + buffer[p][q];
//    }
//    meanBuffer[q]=Float.parseFloat(df.format(frameVal/mChannels));
//}
//
//    AudioFeatureExtraction extraction = new AudioFeatureExtraction();
//    float[] mfccInput = extraction.extractMFCCFeatures(meanBuffer);
//
//    int nMFCC = extraction.getN_mfcc();
//
//    int nFFT = mfccInput.length/nMFCC;
//    double [][] mfccValues = new double[nMFCC][nFFT];
//
//    //loop to convert the mfcc values into multi-dimensional array
//        for(int i=0;i<nFFT;i++){
//    int indexCounter = i * nMFCC;
//    int rowIndexValue = i%nFFT;
//    for(int j=0;j<nMFCC;j++){
//        mfccValues[j][rowIndexValue]=mfccInput[indexCounter];
//        indexCounter++;
//    }
//}
//
//
//    //code to take the mean of mfcc values across the rows such that
//    //[nMFCC x nFFT] matrix would be converted into
//    //[nMFCC x 1] dimension - which would act as an input to tflite model
//    float [] meanMFCCValues = new float[nMFCC];
//        for(int p=0;p<nMFCC;p++){
//    double fftValAcrossRow = 0;
//    for(int q=0;q<nFFT;q++){
//        fftValAcrossRow = fftValAcrossRow + mfccValues[p][q];
//    }
//    double fftMeanValAcrossRow = fftValAcrossRow/nFFT;
//    meanMFCCValues[p] = (float) fftMeanValAcrossRow;
//}
//
//}
