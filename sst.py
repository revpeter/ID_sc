import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(layout = "wide")

## Data import ##
df = pd.read_csv("akaka.csv", index_col=[0])


## Page ##
# Basic describtion
col1, col2, col3 = st.beta_columns([2, 3, 2])
pcol1, pcol2, pcol3 = st.beta_columns([1,3,1])

col2.header("**{}** sor adat van jelenleg az adatbázisban.".format((len(df))))
col2.header("2021. március 5-től kezdve **{}** napja fut a gyüjtés.".format( (len(df["ScDay"].unique()) )))
col2.header("**{}** különböző napról van adat jelenleg.".format( (len(df["Date"].unique()) )))
col2.header("**{}°C** a legmagasabb mérés.".format( df["TempMax"].max() ))
col2.header("**{}°C** a legalacsonyabb mérés.".format( df["TempMin"].min() ))

# The latest values
col2.title("Legfrisebb mérések a következő 15 napra")
lastDay = df["ScDay"].iloc[-1]
col2.write("Minden nap 10 és 22 órakör történik gyüjtés. Emiatt vannak délelötti, délutáni és átlagolt adatok. \
         **A legutolsó gyüjtés {}-án/én {} órakor történt.** ".format(lastDay.replace("-","."), df["ScTime"].iloc[-1]))

stBox1 = col2.selectbox("Napszak kiválasztása", ["Délelött", "Délután", "Átlagolt"], index = 2)

#The latest values Fig
f10 = df["ScTime"] == 10
f22 = df["ScTime"] == 22
fDate = df["ScDay"] == lastDay


if stBox1 == "Átlagolt":
    dfplot_fig1 = df[(f22 | f10) & fDate].groupby("Date", as_index = False, sort = False).mean()
    dfplot_fig1["Day"] = list(df[(f22 | f10) & fDate].drop_duplicates("Date")["Day"])
elif stBox1 == "Délelött":
    dfplot_fig1 = df[f10 & fDate].copy()
elif stBox1 == "Délután":
    dfplot_fig1 = df[f22 & fDate].copy()


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=dfplot_fig1["Date"], y=dfplot_fig1["TempMax"],
                    mode='markers+lines',
                    marker_color = "red",
                    name='Max °C'))

fig1.add_trace(go.Scatter(x=dfplot_fig1["Date"], y=dfplot_fig1["TempMin"],
                    mode='markers+lines',
                    marker_color = "blue",
                    text = dfplot_fig1["Day"],
                    name='Min °C'))

fig1.update_layout(
    plot_bgcolor="#FFF",
    xaxis_linecolor="#000",
    yaxis_linecolor="#000",
    yaxis_title = "°C",
    hovermode="x unified",
    hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.6)", font_color = "#000"),
    margin=dict(l=0,r=0,b=15,t=30,pad=0),
    paper_bgcolor = "#f0f2f6"
)

pcol2.plotly_chart(fig1, use_container_width = True)

#All values for future dates
def ffk(a):
    num = sum(df[df["ScTime"] == 22]["Date"] == a)

    return(a + " - [{} mérés]".format(num))

with st.beta_container():
    col1, col2, col3 = st.beta_columns([2, 3, 2])
    col2.title("A mai naptól következő napokról minden mérés")
    col2.write("Mivel az egyes napokról több nap is készül mérés ezért édemes összehasonlítani az egyes napokon mért értékeket.")

dfSb = df[df["DateFormat"] >= lastDay]

with st.beta_container():
    col1, col2, col3 = st.beta_columns([2, 3, 2])
    sb = col2.selectbox("Nap kiválasztása", dfSb["Date"].unique(), format_func = ffk )

#All values for future dates Fig
dfplot_fig2 = df[(df["Date"] == sb) & (df["ScTime"] == 22)].reset_index()

def anText(a):
    res = []
    for i in range(0,len(a)):
        w1 = str(a.iloc[i]["W1"])
        w2 = str(a.iloc[i]["W2"]).lower()
        if (w1 != "nan") & (w2 != "nan"):
            mm = w1 + ", " + w2
            res.append(mm)
        else:
            res.append(str(w1))
    return res

fig2 = go.Figure()
fig2.add_trace(go.Bar(
            y=dfplot_fig2["ScDay"],
            x=dfplot_fig2["TempMax"],
            text = anText(dfplot_fig2),
            orientation="h",
            name="",
            marker_color = "#FF392E",
            texttemplate='%{text}', textposition='inside'))
fig2.add_trace(go.Bar(
            y=dfplot_fig2["ScDay"],
            x=dfplot_fig2["TempMin"],
            text = dfplot_fig2["ScDay"],
            orientation="h",
            name="",
            marker_color = "#256AE5",
            texttemplate='%{text}', textposition='inside'))

fig2.update_traces(hovertemplate = "%{x}°C", hoverlabel = dict(align = "right"))

fig2.update_layout(
    barmode = "overlay",
    height = 500,
    plot_bgcolor="#FFF",
    xaxis_linecolor="#000",
    xaxis_title = "°C",
    yaxis={'visible': False, 'showticklabels': False},
    margin=dict(l=40,r=40,b=40,t=30,pad=0),
    paper_bgcolor = "#f0f2f6",
    showlegend=False,
    hovermode="y"
)


with st.beta_container():
    pcol1, pcol2, pcol3 = st.beta_columns([1,3,1])
    pcol2.plotly_chart(fig2, use_container_width = True)


