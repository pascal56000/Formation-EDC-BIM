#!/usr/bin/env python3
"""
Uptale Scenario Converter & Automation Package Generator
Converts JSON/Excel pedagogical scenarios into Uptale Studio compatible import formats.
Generates:
 1. Quizzes & Questions CSV (Uptale Bulk Quizzes Format)
 2. Scene Sequence & Voiceover CSV
 3. Media Asset Inventory Manifest
 4. RPA Payload (Playwright / Web Injection format for Uptale Studio)
"""

import sys
import json
import csv
import os
from typing import Dict, Any, List

def process_scenario(input_json_path: str, output_dir: str):
    if not os.path.exists(input_json_path):
        print(f"Error: File {input_json_path} not found.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    module_info = data.get("module_info", {})
    scenes = data.get("scenes", [])

    print(f"Processing Uptale Module: {module_info.get('title', 'Sans Titre')}")
    print(f"Found {len(scenes)} scenes.")

    # 1. Generate Quizzes CSV (Uptale Studio Bulk Quizzes)
    quiz_csv_path = os.path.join(output_dir, "uptale_quizzes_import.csv")
    quiz_rows = []

    # 2. Generate Scene Subtitles / Voiceovers CSV
    voiceover_csv_path = os.path.join(output_dir, "uptale_voiceovers_subtitles.csv")
    voiceover_rows = []

    # 3. Generate Media Inventory Manifest
    manifest_path = os.path.join(output_dir, "uptale_media_manifest.json")
    media_inventory = {
        "photos_360": [],
        "videos_360": [],
        "audio_voiceovers": [],
        "hotspot_images": []
    }

    # 4. RPA Automation Data Structure
    rpa_payload_path = os.path.join(output_dir, "uptale_rpa_payload.json")
    rpa_payload = {
        "module": module_info,
        "scenes_count": len(scenes),
        "actions": []
    }

    for scene_idx, scene in enumerate(scenes, start=1):
        s_id = scene.get("scene_id", f"scene_{scene_idx}")
        s_title = scene.get("title", f"Scène {scene_idx}")
        media_type = scene.get("media_type", "photo_360")
        media_file = scene.get("media_file", "")

        if media_file:
            if "video" in media_type:
                media_inventory["videos_360"].append({"scene_id": s_id, "file": media_file})
            else:
                media_inventory["photos_360"].append({"scene_id": s_id, "file": media_file})

        # Voiceover
        vo = scene.get("voiceover", {})
        if vo.get("text") or vo.get("audio_file"):
            voiceover_rows.append({
                "Scene_ID": s_id,
                "Scene_Title": s_title,
                "Voiceover_Text": vo.get("text", ""),
                "Audio_File": vo.get("audio_file", ""),
                "Auto_Play": "Oui" if vo.get("auto_play", True) else "Non"
            })
            if vo.get("audio_file"):
                media_inventory["audio_voiceovers"].append({"scene_id": s_id, "file": vo.get("audio_file")})

        rpa_scene_action = {
            "step": scene_idx,
            "action": "create_scene",
            "scene_id": s_id,
            "title": s_title,
            "media_type": media_type,
            "media_file": media_file,
            "hotspots": []
        }

        # Hotspots & Quizzes
        for hs_idx, hs in enumerate(scene.get("hotspots", []), start=1):
            hs_id = hs.get("hotspot_id", f"{s_id}_hs_{hs_idx}")
            hs_title = hs.get("title", f"Hotspot {hs_idx}")
            hs_type = hs.get("type", "info_tag")
            pos = hs.get("position", {"yaw": 0, "pitch": 0})
            content = hs.get("content", {})

            if content.get("image_url"):
                media_inventory["hotspot_images"].append({"hotspot_id": hs_id, "file": content.get("image_url")})

            quiz_data = content.get("quiz")
            if hs_type == "quiz_question" and quiz_data:
                q_text = quiz_data.get("question", "")
                q_type = quiz_data.get("question_type", "single_choice")
                options = quiz_data.get("options", [])
                correct_options = [opt.get("text") for opt in options if opt.get("is_correct")]
                all_options = [opt.get("text") for opt in options]

                quiz_rows.append({
                    "Scene_ID": s_id,
                    "Scene_Title": s_title,
                    "Hotspot_Title": hs_title,
                    "Question": q_text,
                    "Type": q_type,
                    "Option_1": all_options[0] if len(all_options) > 0 else "",
                    "Option_2": all_options[1] if len(all_options) > 1 else "",
                    "Option_3": all_options[2] if len(all_options) > 2 else "",
                    "Option_4": all_options[3] if len(all_options) > 3 else "",
                    "Correct_Answers": " | ".join(correct_options),
                    "Points": quiz_data.get("points", 10),
                    "Explanation": quiz_data.get("explanation", "")
                })

            rpa_scene_action["hotspots"].append({
                "hotspot_id": hs_id,
                "title": hs_title,
                "type": hs_type,
                "yaw": pos.get("yaw", 0),
                "pitch": pos.get("pitch", 0),
                "content": content
            })

        rpa_payload["actions"].append(rpa_scene_action)

    # Write Quizzes CSV
    with open(quiz_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ["Scene_ID", "Scene_Title", "Hotspot_Title", "Question", "Type",
                      "Option_1", "Option_2", "Option_3", "Option_4", "Correct_Answers", "Points", "Explanation"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for r in quiz_rows:
            writer.writerow(r)

    # Write Voiceovers CSV
    with open(voiceover_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ["Scene_ID", "Scene_Title", "Voiceover_Text", "Audio_File", "Auto_Play"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for r in voiceover_rows:
            writer.writerow(r)

    # Write Media Manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(media_inventory, f, indent=2, ensure_ascii=False)

    # Write RPA Payload
    with open(rpa_payload_path, 'w', encoding='utf-8') as f:
        json.dump(rpa_payload, f, indent=2, ensure_ascii=False)

    print("\n--- UPTALE CONVERSION SUCCESSFUL ---")
    print(f"1. Import Quizzes CSV      : {quiz_csv_path} ({len(quiz_rows)} questions)")
    print(f"2. Voiceovers & Subtitles  : {voiceover_csv_path} ({len(voiceover_rows)} voix-off)")
    print(f"3. Media Inventory Manifest: {manifest_path}")
    print(f"4. RPA Automation Payload  : {rpa_payload_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uptale_converter.py <scenario_json_path> [output_directory]")
        sys.exit(1)

    json_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "uptale_export"
    process_scenario(json_file, out_dir)
