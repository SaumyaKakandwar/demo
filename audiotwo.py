import streamlit as st
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.spatial.distance import cosine
import librosa.display

# Load and process audio files
def load_audio(file):
    if file is not None:
        try:
            wav, sample_rate = sf.read(file)
            if len(wav.shape) > 1:
                wav = np.mean(wav, axis=1)  # Convert stereo to mono
            return wav, sample_rate
        except Exception as e:
            st.error(f"Error loading audio: {e}")
            return None, None
    return None, None

# Compare voices and compute similarity
def compare_voices(audio1, audio2):
    encoder = VoiceEncoder()

    embed1 = encoder.embed_utterance(preprocess_wav(audio1))
    embed2 = encoder.embed_utterance(preprocess_wav(audio2))

    similarity = np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))
    
    return similarity, embed1, embed2

# Detect fake speech using embeddings
def detect_fake_speech(embed1, embed2):
    distance = cosine(embed1, embed2)
    return distance

# Visualize embeddings using PCA
def visualize_pca_embeddings(embed1, embed2):
    pca = PCA(n_components=2)
    embeddings = np.vstack([embed1, embed2])

    reduced_embeddings = pca.fit_transform(embeddings)

    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_embeddings[0, 0], reduced_embeddings[0, 1], color="blue", label="Audio 1")
    plt.scatter(reduced_embeddings[1, 0], reduced_embeddings[1, 1], color="red", label="Audio 2")

    plt.title("2D PCA of Audio Embeddings")
    plt.legend()
    st.pyplot(plt)

# Visualize embeddings using t-SNE
def visualize_tsne_embeddings(embed1, embed2):
    embeddings = np.vstack([embed1, embed2])
    n_samples = embeddings.shape[0]

    # Ensure perplexity is less than the number of samples
    perplexity = min(5, n_samples - 1)  # Example: use min to set a reasonable perplexity

    if perplexity <= 0:
        perplexity = 1  # Set a minimum value for perplexity

    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    reduced_embeddings = tsne.fit_transform(embeddings)

    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_embeddings[0, 0], reduced_embeddings[0, 1], color="blue", label="Audio 1")
    plt.scatter(reduced_embeddings[1, 0], reduced_embeddings[1, 1], color="red", label="Audio 2")

    plt.title("2D t-SNE of Audio Embeddings")
    plt.legend()
    st.pyplot(plt)

# Visualize embedding differences
def visualize_embedding_differences(embed1, embed2):
    difference = np.abs(embed1 - embed2)
    plt.figure(figsize=(10, 4))
    sns.heatmap(difference.reshape(1, -1), cmap="coolwarm", cbar=True)
    plt.title("Absolute Differences in Embeddings")
    st.pyplot(plt)

# Visualize fake speech detection
def visualize_fake_speech_detection(embed1, embed2):
    distance = detect_fake_speech(embed1, embed2)
    plt.figure(figsize=(6, 4))
    sns.barplot(x=['Distance'], y=[distance], palette='viridis')
    plt.title("Cosine Distance for Fake Speech Detection")
    st.pyplot(plt)

# Visualize waveforms
def visualize_waveforms(wav1, wav2):
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(wav1, alpha=0.5, color='blue')
    plt.title("Waveform of Audio 1")
    
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(wav2, alpha=0.5, color='red')
    plt.title("Waveform of Audio 2")

    st.pyplot(plt)

# Visualize spectrograms
def visualize_spectrograms(wav1, wav2, sample_rate):
    plt.figure(figsize=(14, 8))
    
    plt.subplot(2, 1, 1)
    D1 = np.abs(librosa.stft(wav1))
    librosa.display.specshow(librosa.amplitude_to_db(D1, ref=np.max), sr=sample_rate, y_axis='log', x_axis='time')
    plt.title("Spectrogram of Audio 1")
    plt.colorbar(format='%+2.0f dB')
    
    plt.subplot(2, 1, 2)
    D2 = np.abs(librosa.stft(wav2))
    librosa.display.specshow(librosa.amplitude_to_db(D2, ref=np.max), sr=sample_rate, y_axis='log', x_axis='time')
    plt.title("Spectrogram of Audio 2")
    plt.colorbar(format='%+2.0f dB')

    st.pyplot(plt)

# Streamlit UI
def main():
    st.title("TSS AUDIO COMPARISON TOOL")
    st.write("Upload two audio files to compare their voice embeddings, detect fake speech, and visualize the results.")

    audio_file1 = st.file_uploader("Upload first audio file", type=["wav", "mp3", "flac", "ogg"])
    audio_file2 = st.file_uploader("Upload second audio file", type=["wav", "mp3", "flac", "ogg"])

    if audio_file1 and audio_file2:
        wav1, sample_rate1 = load_audio(audio_file1)
        wav2, sample_rate2 = load_audio(audio_file2)

        if wav1 is not None and wav2 is not None:
            if st.button("Analyze"):
                try:
                    # Compare the voices and get embeddings
                    similarity_score, embed1, embed2 = compare_voices(wav1, wav2)

                    # Display the similarity score
                    st.write(f"Voice similarity score: **{similarity_score:.4f}**")

                    if similarity_score >= 0.85:
                        st.success("The voices are **very similar**.")
                    elif 0.7 <= similarity_score < 0.85:
                        st.warning("The voices are **somewhat similar**.")
                    else:
                        st.error("The voices are **different**.")

                    # Visualizations
                    st.write("### PCA Visualization of Embeddings")
                    visualize_pca_embeddings(embed1, embed2)

                    st.write("### t-SNE Visualization of Embeddings")
                    visualize_tsne_embeddings(embed1, embed2)

                    st.write("### Embedding Difference Heatmap")
                    visualize_embedding_differences(embed1, embed2)

                    st.write("### Fake Speech Detection Bar Chart")
                    visualize_fake_speech_detection(embed1, embed2)

                    st.write("### Waveforms of Audio Files")
                    visualize_waveforms(wav1, wav2)

                    st.write("### Spectrograms of Audio Files")
                    visualize_spectrograms(wav1, wav2, sample_rate1)

                except Exception as e:
                    st.error(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
