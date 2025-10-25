import streamlit as st
import pandas as pd
import sqlite3

st.title("Economize de Verdade nas Suas Compras de Supermercado em São José dos Campos!")
st.markdown(body="### Compare seu carrinho de compras e descubra o supermercado mais barato perto de você. Chega de pagar caro!")
st.divider()
st.sidebar.image(image=r"C:\Users\Matheus Pigatto\Pictures\carrinho_compra.JPG",width=100)
st.sidebar.markdown(body='# :memo: Menu')

st.sidebar.divider()
st.sidebar.page_link("pages/01_home.py", label="Home")
st.sidebar.page_link("pages/sobre_nos.py", label="Sobre")
st.sidebar.page_link("pages/como_funciona.py", label="Como Funciona")
st.sidebar.page_link("pages/comparar_listas.py", label= "Comparador")
st.sidebar.page_link("pages/contato.py", label= "Contato")
