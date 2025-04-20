import streamlit as st
import json
import requests
import os
import pandas as pd
 # ✅ Correct import

# Set page title & icon
st.set_page_config(page_title="Library Manager", page_icon="📔")
# File to store book data
LIBRARY_FILE = "Aqib_books.json"

# ✅ Load Library Function
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# ✅ Save Library Function
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# ✅ Load Lottie Animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# ✅ Add Book Function
def add_book(library):
    st.header("➕ Add Book")
    with st.form("add_book_form"):
        title = st.text_input("Enter the book title:")
        author = st.text_input("Enter the author:")
        year = st.number_input("Enter the publication year:", min_value=0, step=1)
        genre = st.text_input("Enter the genre:")
        read_status = st.checkbox("Have you read this book?")
        submitted = st.form_submit_button("🥰 Add Book")
        
        if submitted:
            book = {
                "Title": title,
                "Author": author,
                "Year": int(year),
                "Genre": genre,
                "Read": read_status
            }
            library.append(book)
            save_library(library)
            st.success("Book added successfully!")
            st.balloons()

# ✅ Remove Book Function
def remove_book(library):
    st.header("🗑 Remove a Book")
    title = st.text_input("Enter the title of the book to remove:")
    
    if st.button("🗑 Remove Book"):
        for book in library:
            if book["Title"].lower() == title.lower():
                library.remove(book)
                save_library(library)
                st.success("Book removed successfully!")
                return
        st.error("Book not found.")

# ✅ Search Book Function
def search_book(library):
    st.header("🔍 Search Book")
    search_type = st.radio("Search by:", ("Title", "Author"))
    keyword = st.text_input("Enter search term:")
    
    if st.button("🔍 Search"):
        if keyword.strip():
            results = [book for book in library if keyword.lower() in book[search_type].lower()]
            if results:
                df = pd.DataFrame(results)
                st.table(df)

            else:
                st.error("No matching books found.")
        else:
            st.warning("Please enter a search term.")

# ✅ Display Books Function
def display_books(library):
    st.header("💽 Display Books")
    if not library:
        st.warning("No books in your library.")
    else:
        for book in library:
            st.write(f"*{book['Title']}* by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✅ Read' if book['Read'] else '❌ Unread'}")

# ✅ Display Statistics Function
def display_statistics(library):
    st.header("📊 Library Statistics")
    total_books = len(library)
    
    if total_books == 0:
        st.warning("No books in your library.")
        return
    
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books) * 100
    
    st.write(f"📚 *Total books:* {total_books}")
    st.write(f"📖 *Books Read:* {read_books}")
    st.write(f"📊 *Percentage Read:* {percentage_read:.2f}%")

def sidebar_animation():
    with st.sidebar:
        st.header("📖 Welcome to Library")



# ✅ Main Function
def main():
    st.title("📚 Personal Library Manager")
    st.header("🥰 Created by Aqib**")
    sidebar_animation()
    library = load_library()
    
    option = st.sidebar.selectbox(" Menu", ["➕ Add a book", "🗑 Remove a book", "🔍 Search for a book", "💽 Display all books", "📊 Display statistics"])
    
    if option == "➕ Add a book":
        add_book(library)
    elif option == "🗑 Remove a book":
        remove_book(library)
    elif option == "🔍 Search for a book":
        search_book(library)
    elif option == "💽 Display all books":
        display_books(library)
    elif option == "📊 Display statistics":
        display_statistics(library)

# ✅ Run the app

main()