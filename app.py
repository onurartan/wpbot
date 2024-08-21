import os
import json
import streamlit as st
from func import (
    load_groups_with_titles,
    save_group,
    delete_group,
    load_ready_messages,
    save_ready_message
)
from runbot import run_bot

GROUPS_FILE = "groups.json"
READY_MESSAGES_FILE = "ready_message.json"


def load_groups_with_titles():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                st.error("Gruplar yüklenirken bir hata oluştu. Dosya bozulmuş olabilir.")
                return []
    return []


def get_group_options(title):
    data = load_groups_with_titles()
    for entry in data:
        if entry["groupTitle"] == title:
            return entry["groups"]
    return []


st.title("WhatsApp Bot Yönetim Paneli (by Onur Artan)")

tabs = st.tabs(["Grup Yönetimi", "Hazır Mesajlar", "Botu Çalıştır"])

# Grup Yönetimi Tab
with tabs[0]:
    st.header("Grup Yönetimi")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Yeni Başlık ve Grup Ekle")
        new_group_title = st.text_input("Yeni Başlık")
        new_group_name = st.text_input("Yeni Grup")
        if st.button("Grup Ekle"):
            if new_group_title and new_group_name:
                save_group(new_group_title, new_group_name)
                st.success(f"'{new_group_name}' grubu '{new_group_title}' başlığı altında başarıyla eklendi.")
            else:
                st.error("Başlık ve grup adı boş olamaz.")

    with col2:
        st.subheader("Grup Sil")
        data = load_groups_with_titles()
        titles = [entry["groupTitle"] for entry in data]
        selected_title = st.selectbox("Silinecek Başlık Seçin", titles)
        if selected_title:
            groups = get_group_options(selected_title)
            group_to_delete = st.selectbox("Silinecek Grubu Seçin", groups)
            if st.button("Grubu Sil"):
                if group_to_delete:
                    delete_group(selected_title, group_to_delete)
                    st.success(f"'{group_to_delete}' grubu başarıyla silindi.")
                else:
                    st.error("Silinecek grup seçilmedi.")

    st.subheader("Kayıtlı Gruplar")
    data = load_groups_with_titles()
    if data:
        for entry in data:
            st.write(f"Başlık: {entry['groupTitle']}")
            st.write("Gruplar:")
            for group in entry["groups"]:
                st.write(f"- {group}")
    else:
        st.write("Henüz Kayıtlı grup yok.")

# Hazır Mesajlar Tab
with tabs[1]:
    st.header("Hazır Mesajlar")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Yeni Hazır Mesaj Ekle")
        new_ready_message = st.text_input("Yeni Hazır Mesaj")
        if st.button("Mesaj Ekle"):
            if new_ready_message:
                save_ready_message(new_ready_message)
                st.success(f"'{new_ready_message}' mesajı başarıyla eklendi.")
            else:
                st.error("Mesaj boş olamaz.")

    with col2:
        st.subheader("Hazır Mesajlar")
        messages = load_ready_messages()
        if messages:
            message_options = [msg["message"] for msg in messages]
            selected_message = st.selectbox("Hazır Mesaj Seçin", message_options)
        else:
            st.write("Hazır mesaj bulunmuyor.")
            selected_message = ""

# Botu Çalıştır Tab
with tabs[2]:
    st.header("Botu Çalıştır")

    data = load_groups_with_titles()
    titles = [entry["groupTitle"] for entry in data]
    selected_title = st.selectbox("Grup Başlığı Seçin", titles)
    if selected_title:
        group_options = get_group_options(selected_title)
        selected_groups = st.multiselect("Grup Seçin", group_options)
    else:
        selected_groups = []

    message = st.text_area("Gönderilecek Mesaj", value=selected_message if selected_message else "")

    if st.button("Botu Çalıştır"):
        if not selected_groups:
            st.error("Mesaj gönderilecek grup seçilmedi!")
        elif not message:
            st.error("Gönderilecek mesajı yazmalısınız!")
        else:
            run_bot(selected_groups, message)
            st.success("Bot başarıyla çalıştırıldı.")
