import asyncio
import os
import shutil
import subprocess
import edge_tts

WORKDIR = os.path.dirname(os.path.abspath(__file__))
BUILDDIR = os.path.join(WORKDIR, "vsl_build")
os.makedirs(BUILDDIR, exist_ok=True)

VOICE = "en-US-JennyNeural"

SCENES = [
    {
        "index": 0,
        "name": "00_presenter_hook",
        "type": "avatar",
        "shot": "wide",
        "text": "If you own or manage properties with Section 8 or HUD housing vouchers, the rules for your property inspections have completely changed under the new NSPIRE federal standards.",
        "subtitle": "If you own or manage properties with Section 8 or HUD vouchers,\\Nthe rules for your property inspections have completely changed\\Nunder the new NSPIRE federal standards.",
    },
    {
        "index": 1,
        "name": "01_broll_checklist",
        "type": "broll",
        "source": os.path.join(WORKDIR, "checklist_broll.jpg"),
        "text": "Under the new rules, minor oversights like an expired smoke alarm, a missing GFCI outlet within six feet of a sink, or an improper water heater discharge pipe trigger an automatic twenty-four hour emergency repair order.",
        "subtitle": "Minor oversights like a missing GFCI outlet within 6 feet of water,\\Nan unsealed smoke alarm, or an improper water heater discharge pipe\\ntrigger an automatic 24-hour emergency repair order.",
        "motion": "pan_up"
    },
    {
        "index": 2,
        "name": "02_presenter_stakes",
        "type": "avatar",
        "shot": "close_up",
        "text": "And if those items are not cleared immediately, HUD can freeze your monthly rental subsidies. Most landlords don't fail because their properties are bad—they fail because they didn't know what the inspector was looking for.",
        "subtitle": "If those items are not cleared immediately,\\NHUD can freeze your monthly rental subsidies.\\nMost landlords fail simply because they didn't know\\nwhat the inspector was looking for.",
    },
    {
        "index": 3,
        "name": "03_broll_calculator",
        "type": "broll",
        "source": os.path.join(WORKDIR, "calculator_broll.jpg"),
        "text": "The NSPIRE Compliance Kit gives you the exact pre-inspection self-audit checklist, the top twenty-five immediate failure guide, and the automated NSPIRE scoring calculator to walk your building before the inspector knocks on your door.",
        "subtitle": "The NSPIRE Compliance Kit gives you the exact self-audit checklist,\\nthe top 25 immediate failure guide, and the automated NSPIRE scoring model\\nto walk your building before the inspector knocks on your door.",
        "motion": "zoom_in"
    },
    {
        "index": 4,
        "name": "04_presenter_cta",
        "type": "avatar",
        "shot": "medium_push",
        "text": "You can catch and fix simple maintenance defects in advance, protect your inspection score, and keep your rental income completely safe. Review the complete inspection package below for instant download.",
        "subtitle": "Catch and fix simple maintenance defects in advance,\\nprotect your inspection score, and keep your rental income completely safe.\\nReview the complete inspection package below for instant download.",
    }
]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def create_subtitles_ass(scenes, out_file):
    header = """[Script Info]
Title: NSPIRE Compliance Kit Official Briefing
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,28,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,3,2,0,2,40,40,32,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    current_time = 0.0
    for sc in scenes:
        start_str = format_ass_time(current_time + 0.1)
        end_str = format_ass_time(current_time + sc["dur"] - 0.1)
        text = sc["subtitle"].replace("\n", "\\N")
        events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{text}")
        current_time += sc["dur"]

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"[OK] Created ASS subtitles: {out_file} (Total: {current_time:.2f}s)")
    return current_time

async def generate_audio():
    print(f"[*] Generating Voiceover Audio with {VOICE}...")
    for idx, sc in enumerate(SCENES):
        audio_mp3 = os.path.join(BUILDDIR, f"audio_{idx:02d}.mp3")
        audio_wav = os.path.join(BUILDDIR, f"audio_{idx:02d}.wav")
        comm = edge_tts.Communicate(sc["text"], VOICE, rate="+3%", pitch="+0Hz")
        await comm.save(audio_mp3)
        
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_mp3,
            "-ac", "2", "-ar", "48000", audio_wav
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", audio_wav
        ], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        sc["audio_dur"] = dur
        sc["dur"] = max(dur + 0.4, 6.0)
        print(f"    [OK] Scene {idx}: '{sc['name']}' -> audio {dur:.2f}s, target scene {sc['dur']:.2f}s")

def build_scene_video(sc, raw_avatar):
    idx = sc["index"]
    target_dur = sc["dur"]
    out_video = os.path.join(BUILDDIR, f"clean_video_{idx:02d}.mp4")
    out_audio = os.path.join(BUILDDIR, f"clean_audio_{idx:02d}.wav")
    
    # Audio padding to exact target duration
    src_audio = os.path.join(BUILDDIR, f"audio_{idx:02d}.wav")
    cmd_a = [
        "ffmpeg", "-y",
        "-i", src_audio,
        "-af", f"apad=whole_dur={target_dur:.2f}",
        "-t", f"{target_dur:.2f}",
        "-ac", "2",
        "-ar", "48000",
        out_audio
    ]
    subprocess.run(cmd_a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if sc["type"] == "avatar":
        # Video stream from speaking neural avatar
        shot = sc.get("shot", "wide")
        fps = 24
        total_frames = int(target_dur * fps)
        
        if shot == "wide":
            # Multi-camera wide: pristine full frame
            vf = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24"
        elif shot == "close_up":
            # Multi-camera close-up: subtle crop punch-in for intensity
            vf = "scale=1440:810,crop=1280:720:80:45,setsar=1,fps=24"
        elif shot == "medium_push":
            # Multi-camera call to action: gentle push-in
            vf = f"scale=1280:720,zoompan=z='min(zoom+0.0004,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1280x720:fps=24"
        else:
            vf = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24"
            
        cmd_v = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", raw_avatar,
            "-vf", vf,
            "-t", f"{target_dur:.2f}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "19",
            "-pix_fmt", "yuv420p",
            "-an",
            out_video
        ]
        subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # B-roll with dynamic Ken Burns document tracking
        fps = 24
        total_frames = int(target_dur * fps)
        if sc.get("motion") == "zoom_in":
            vf = f"scale=1920:1080,zoompan=z='min(zoom+0.0006,1.18)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1280x720:fps={fps}"
        elif sc.get("motion") == "zoom_out":
            vf = f"scale=1920:1080,zoompan=z='max(1.18-0.0006*on,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1280x720:fps={fps}"
        else:
            vf = f"scale=1920:1080,zoompan=z='1.12':x='iw/2-(iw/zoom/2)':y='ih*0.2+(ih*0.1*on/{total_frames})':d={total_frames}:s=1280x720:fps={fps}"
            
        cmd_v = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", sc["source"],
            "-vf", vf,
            "-t", f"{target_dur:.2f}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "19",
            "-pix_fmt", "yuv420p",
            "-an",
            out_video
        ]
        subprocess.run(cmd_v, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    return out_video, out_audio

def assemble_master_vsl():
    raw_avatar = os.path.join(BUILDDIR, "raw_avatar_00.mp4")
    if not os.path.exists(raw_avatar):
        raise FileNotFoundError(f"Missing master avatar source at: {raw_avatar}")
        
    total_dur = create_subtitles_ass(SCENES, os.path.join(BUILDDIR, "subtitles.ass"))
    video_files = []
    audio_files = []
    
    for sc in SCENES:
        print(f"[*] Processing Scene {sc['index']}: {sc['name']} ({sc['dur']:.2f}s, type={sc['type']})...")
        v, a = build_scene_video(sc, raw_avatar)
        video_files.append(v)
        audio_files.append(a)
        
    concat_v_txt = os.path.join(BUILDDIR, "concat_clean_videos.txt")
    with open(concat_v_txt, "w") as f:
        for vf in video_files:
            f.write(f"file '{vf}'\n")
            
    concat_a_txt = os.path.join(BUILDDIR, "concat_clean_audio.txt")
    with open(concat_a_txt, "w") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")
            
    combined_v = os.path.join(BUILDDIR, "combined_clean_visuals.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_v_txt,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        combined_v
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    combined_a = os.path.join(BUILDDIR, "combined_clean_audio.wav")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_a_txt,
        "-c", "copy",
        combined_a
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    music_bed = r"C:\Users\fores\.gemini\antigravity\scratch\agency-website\veo_vsl_build\music_bed.wav"
    has_music = os.path.exists(music_bed)
    
    final_output = "nspire_briefing.mp4"
    sub_path = "vsl_build/subtitles.ass"
    
    print("[*] Muxing final video with subtitles and background mix...")
    if has_music:
        filter_complex = f"[0:v]subtitles='{sub_path}'[v];[2:a]volume=0.10[bg];[1:a][bg]amix=inputs=2:duration=first:dropout_transition=2[a]"
        cmd = [
            "ffmpeg", "-y",
            "-i", combined_v,
            "-i", combined_a,
            "-stream_loop", "-1", "-i", music_bed,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_dur:.2f}",
            final_output
        ]
    else:
        filter_complex = f"[0:v]subtitles='{sub_path}'[v]"
        cmd = [
            "ffmpeg", "-y",
            "-i", combined_v,
            "-i", combined_a,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_dur:.2f}",
            final_output
        ]
        
    subprocess.run(cmd, check=True)
    print(f"\n[+] Master Speaking Avatar NSPIRE Video generated successfully: {final_output}")
    print(f"[+] Total Duration: {total_dur:.2f}s (~{total_dur/60:.1f} minutes)")

if __name__ == "__main__":
    asyncio.run(generate_audio())
    assemble_master_vsl()
