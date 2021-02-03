import be.tarsos.dsp.AudioDispatcher;
import be.tarsos.dsp.io.TarsosDSPAudioInputStream;
import be.tarsos.dsp.io.jvm.JVMAudioInputStream;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.UnsupportedAudioFileException;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.io.File;
import java.io.IOException;
import java.math.RoundingMode;
import java.text.DecimalFormat;

import com.jlibrosa.audio.wavFile.WavFile;
import com.jlibrosa.audio.wavFile.WavFileException;
import com.jlibrosa.audio.process.AudioFeatureExtraction;


import org.opencv.core.Mat;

public class ProjectMain
{
    public static void main(String[] args) throws IOException, WavFileException
    {
//        File initialFile = new File("D:/Users/Owen/Final_Year_Project/recordings/Ireland/Common_Wood_Pigeon/372363/XC372363-Columba_palumbus_Dublin_1518.mp3");
//        try
//        {
//            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(initialFile);
//            TarsosDSPAudioInputStream tarsosDSPAudioInputStream = new JVMAudioInputStream(audioInputStream);
//            AudioDispatcher dispatcher = new AudioDispatcher(tarsosDSPAudioInputStream, 2046, 2046);
//            dispatcher.run();
//        }
//        catch (UnsupportedAudioFileException | IOException e)
//        {
//            e.printStackTrace();
//        }
        int mNumFrames;
        int mSampleRate;
        int mChannels;

        File sourceFile = new File("D:/Users/Owen/Final_Year_Project/birdsong/Common_Wood_Pigeon/Common_Wood_Pigeon_0.wav");

        WavFile wavFile = WavFile.openWavFile(sourceFile);
        mNumFrames = (int) wavFile.getNumFrames();
        mSampleRate = (int) wavFile.getSampleRate();
        mChannels = wavFile.getNumChannels();

        float[][] buffer = new float[mChannels][mNumFrames];
        int frameOffset = 0;
        int loopCounter = ((mNumFrames * mChannels)/4096) + 1;
        for (int i = 0; i < loopCounter; i++) {
            frameOffset = wavFile.readFrames(buffer, mNumFrames, frameOffset);
        }


        DecimalFormat df = new DecimalFormat("#.#####");
        df.setRoundingMode(RoundingMode.CEILING);

        float [] meanBuffer = new float[mNumFrames];
        for(int q=0;q<mNumFrames;q++){
            double frameVal = 0;
            for(int p=0;p<mChannels;p++){
                frameVal = frameVal + buffer[p][q];
            }
            meanBuffer[q]=Float.parseFloat(df.format(frameVal/mChannels));
        }

        AudioFeatureExtraction extraction = new AudioFeatureExtraction();
        float[] mfccInput = extraction.extractMFCCFeatures(meanBuffer);

        int nMFCC = extraction.getN_mfcc();

        int nFFT = mfccInput.length/nMFCC;
        double [][] mfccValues = new double[nMFCC][nFFT];

        //loop to convert the mfcc values into multi-dimensional array
        for(int i=0;i<nFFT;i++){
            int indexCounter = i * nMFCC;
            int rowIndexValue = i%nFFT;
            for(int j=0;j<nMFCC;j++){
                mfccValues[j][rowIndexValue]=mfccInput[indexCounter];
                indexCounter++;
            }
        }


        //code to take the mean of mfcc values across the rows such that
        //[nMFCC x nFFT] matrix would be converted into
        //[nMFCC x 1] dimension - which would act as an input to tflite model
        float [] meanMFCCValues = new float[nMFCC];
        for(int p=0;p<nMFCC;p++){
            double fftValAcrossRow = 0;
            for(int q=0;q<nFFT;q++){
                fftValAcrossRow = fftValAcrossRow + mfccValues[p][q];
            }
            double fftMeanValAcrossRow = fftValAcrossRow/nFFT;
            meanMFCCValues[p] = (float) fftMeanValAcrossRow;
        }



    }
}
