"""
YouTube Audience Reception Scraper
----------------------------------
Extracts user comments from specific news videos regarding China-EU relations.
Handles French character encoding (utf-8-sig) for seamless CSV integration.
Requires: pip install youtube-comment-downloader
"""

import csv
import os
from youtube_comment_downloader import YoutubeCommentDownloader

def fetch_youtube_comments(video_url, output_csv_path):
    """
    Downloads all comments from a given YouTube video URL and saves to CSV.
    """
    print(f"Initializing downloader for video: {video_url}")
    downloader = YoutubeCommentDownloader()
    
    comments = []
    # sort_by=1 fetches comments by newest first
    for comment in downloader.get_comments_from_url(video_url, sort_by=1):
        comments.append(comment['text'])
        
    if not comments:
        print("No comments found or video is restricted.")
        return

    # Export to CSV with utf-8-sig to prevent French accent corruption in Excel
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Comment_Text"])
        for comment in comments:
            writer.writerow([comment])
            
    print(f"Success! Exported {len(comments)} comments to {output_csv_path}")

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    pass
    # target_video_url = 'https://www.youtube.com/watch?v=G1E2OV2MAfU'
    # output_file = "../../data/raw/youtube/RTL_EV_Tariffs_Comments.csv"
    # fetch_youtube_comments(target_video_url, output_file)
