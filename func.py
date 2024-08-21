import os
import json
import streamlit as st

GROUPS_FILE = "groups.json"
READY_MESSAGES_FILE = "ready_message.json"

# --------- Grupları Getir --------- #
def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# --------- Yeni Grup --------- #
def save_group(group_title: str, group_name: str):
    data = load_groups()
    for item in data:
        if item["groupTitle"] == group_title:
            if group_name in item["groups"]:
                st.error(f"'{group_name}' zaten mevcut.")
                return
            item["groups"].append(group_name)
            break
    else:
        data.append({"groupTitle": group_title, "groups": [group_name]})

    with open(GROUPS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    st.success(f"'{group_name}' grubu başarıyla eklendi.")

# --------- Grup Sil --------- #
def delete_group(group_title: str, group_name: str):
    data = load_groups()
    for item in data:
        if item["groupTitle"] == group_title and group_name in item["groups"]:
            item["groups"].remove(group_name)
            if not item["groups"]:
                data.remove(item)
            break

    with open(GROUPS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    st.success(f"'{group_name}' grubu başarıyla silindi.")

# --------- Hazır Mesajları getir --------- #
def load_ready_messages():
    try:
        with open(READY_MESSAGES_FILE, "r", encoding="utf-8") as file:
            messages = json.load(file)
        return messages
    except Exception as e:
        st.error(f"Mesajlar yüklenirken bir hata oluştu: {e}")
        return []


def load_groups_with_titles():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r", encoding="utf-8") as file:
            file_content = file.read()
            if file_content.strip() == "":  # Dosya boşsa
                st.error("Gruplar dosyası boş.")
                return []
            try:
                data = json.loads(file_content)
                return data
            except json.JSONDecodeError as e:
                st.error(f"JSON yüklenirken bir hata oluştu: {e}")
                return []
    else:
        st.error("Gruplar dosyası bulunamadı.")
        return []


# --------- Hazır Mesaj Ekle --------- #
def save_ready_message(new_message):
    messages = load_ready_messages()
    new_message_id = max([msg["messageId"] for msg in messages], default=0) + 1
    messages.append({"messageId": new_message_id, "message": new_message})
    try:
        with open(READY_MESSAGES_FILE, "w", encoding="utf-8") as file:
            json.dump(messages, file, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Mesaj kaydedilirken bir hata oluştu: {e}")
