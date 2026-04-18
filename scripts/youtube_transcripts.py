from youtube_transcript_api import YouTubeTranscriptApi
import os

video_id = "L2baqhX1sMg"

transcript = YouTubeTranscriptApi.get_transcript(video_id)

os.makedirs("research/youtube-transcripts", exist_ok=True)

with open("research/youtube-transcripts/chris-walker-video1.md", "w") as f:
    f.write("# Chris Walker Transcript\n\n")

    for row in transcript:
        f.write(row["text"] + "\n")

print("Transcript saved!")