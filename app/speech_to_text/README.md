## References
> https://github.com/mozilla-ai/llamafile/releases
> https://github.com/mozilla-ai/llamafile/blob/main/docs/whisperfile/index.md
> https://huggingface.co/ggerganov/whisper.cpp/tree/main
> https://github.com/mozilla-ai/llamafile/discussions/551

## Usage
Transcribes WAV, MP3, FLAC, and Ogg Vorbis audio
```
# transcribe a local audio file
whisperfile -m whisper-tiny.en-q5_1.bin audio.wav
```

## Improvements:
- [ ] consider adding --gpu auto for gou acceleration? or using a smaller model
