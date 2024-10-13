
#######################################################
# 1. Getting setup -- using our HF template
#######################################################

# We have a few options for how to proceed.  I'll start by showing the process in 
#   PL and then I'll move to my local installation of my template so that I can make 
#   sure I am pushing code at various intervals so folks can check that out.

# NOTE: during this process, you can click on "Always Rerun" for automatic updates.

# See the class notes on this with some photos for reference!
# **this has to be implemented!**


###################################################################
# 2. Review of where we got to last time, in template app.py file
###################################################################


# Let's start by copying things we did last time
import streamlit as st
import altair as alt

# Let's recall a plot that we made with Altair in Jupyterlab:
#    Make sure we copy the URL as well!
mobility_url = 'https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/mobility.csv'

st.title('This is my fancy app for HuggingFace!!')

scatters = alt.Chart(mobility_url).mark_point().encode(
    x='Mobility:Q', # "Q for quantiative"
    #y='Population:Q',
    y=alt.Y('Population:Q', scale=alt.Scale(type='log')),
    color=alt.Color('Income:Q', scale=alt.Scale(scheme='sinebow'),bin=alt.Bin(maxbins=5))
)

st.header('More complex Dashboards')

brush = alt.selection_interval(encodings=['x','y'])

chart1 = alt.Chart(mobility_url).mark_rect().encode(
    alt.X("Student_teacher_ratio:Q", bin=alt.Bin(maxbins=10)),
    alt.Y("State:O"),
    alt.Color("count()")
).properties(
   height=400
).add_params(
        brush
)

chart2 = alt.Chart(mobility_url).mark_bar().encode(
    alt.X("Mobility:Q", bin=True,axis=alt.Axis(title='Mobility Score')),
    alt.Y('count()', axis=alt.Axis(title='Mobility Score Distribution'))
).transform_filter(
    brush
)

chart = (chart1.properties(width=300) | chart2.properties(width=300))

tab1, tab2 = st.tabs(["Mobility interactive", "Scatter plot"])

with tab1:
    st.altair_chart(chart, theme=None, use_container_width=True)
with tab2:
    st.altair_chart(scatters, theme=None, use_container_width=True)


################################################
# 3. Adding features, Pushing to HF
################################################

st.header('Requirements, README file, Pushing to HuggingFace')

### 3.1 Make a plot ###

# Let's say we want to add in some matplotlib plots from some data we read
#  in with Pandas.

import pandas as pd
df = pd.read_csv(mobility_url)

# There are a few ways to show the dataframe if we want our viewer to see the table:
#df
st.write(df)

# Now, let's plot with matplotlib:
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
df['Seg_income'].plot(kind='hist', ax=ax)
#plt.show() # but wait! this doesn't work!  

# We need to use the streamlit-specific way of showing matplotlib plots: https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
st.pyplot(fig)

### 3.2 Push these changes to HF -- requirements.txt ###
# In order to push these changes to HF and have things actually show up we need to 
#   add the packages we've added to our requirements.txt file.

st.write('''The requirements.txt file contains all the packages needed 
         for our app to run.  These include (for our application):''')
st.code('''
streamlit==1.39.0
altair
numpy
pandas
matplotlib
            ''')

# NOTE: for any package you want to use in your app.py file, you must include it in 
#   the requirements.txt file!

# Note #2: we specified a version of streamlit so we can use some specific widgets

### 3.3 Push these changes to HF -- README.md ###

# While we're doing this, let's also take a look at the README.md file!

st.header('Build in HF: README.md & requirements.txt files')

st.code('''
---
title: Prep notebook -- My Streamlit App     
emoji: 🏢
colorFrom: blue   
colorTo: gray
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---
''')
st.write("Note: the sdk version has to match what is in your requirements.txt (and with whatever widgets you want to be able to use).")

# Some important things to note here:

st.write('Some important items to note about these:')
st.markdown('''
* the "emoji" is what will show up as an identifier on your homepage
* the sdk *must* be streamlit
* the "app_file" *must* link to the app file you are developing in
            ''')

################################################
# 4. TODO Quick intro to widgets
################################################

st.header('Widgets in Streamlit apps')

### 4.1 Widget basics: A few widget examples ###

st.markdown("""
These will be very similar to how we used the `ipywidgets` package in Jupyter notebooks.
         """)

st.markdown("""
We won't go over all of them, but you can check out the [list of widgets](https://docs.streamlit.io/develop/api-reference/widgets) 
            linked.
""")

st.markdown("""Let's try a few!""")

st.subheader('Feedback Widget')

st.markdown("""
For example, we could try the [feedback widget](https://docs.streamlit.io/develop/api-reference/widgets/st.feedback).
            """
)
st.markdown("""            
            If we check out the docs for this widget, we see some familiar looking functions like 
            `on_change` and the example they give looks very similar to an 
            "observation" function that we built before using widgets:
             """)

st.code(
"""
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
""")

# Let's give this a shot!

st.write("How great are you feeling right now?")
sentiment_mapping = ["one", "two", "three", "four", "five"] # map to these numers
selected = st.feedback("stars")
if selected is not None: # make sure we have a selection
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
    if selected < 1:
        st.markdown('Sorry to hear you are so sad :(')
    elif selected < 3:
        st.markdown('A solid medium is great!')
    else:
        st.markdown('Fantastic you are having such a great day!')

st.subheader('Radio Buttons')

st.markdown("""
Let's try out a [radio button](https://docs.streamlit.io/develop/api-reference/widgets/st.radio) example.
""")

favoriteViz = st.radio(
    "What's your visualization tool so far?",
    [":rainbow[Streamlit]", "vega-lite :sparkles:", "matplotlib :material/Home:"],
    captions=[
        "New and cool!",
        "So sparkly.",
        "Familiar and comforting.",
    ],
)

if favoriteViz == ":rainbow[Streamlit]":
    st.write("You selected Streamlit!")
else:
    st.write("You didn't select Streamlit but that's ok, Data Viz still likes you :grin:")

st.markdown("""
Note here that we made use of text highlight [colors](https://docs.streamlit.io/develop/api-reference/text/st.markdown) 
            and [emoji's](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/) 
            and [icons](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded).
 """)

### 4.2 Connecting widgets with plots ###

st.subheader('Connecting Widgets and Plots')


st.markdown("""
There are actually [many types of charts](https://docs.streamlit.io/develop/api-reference/charts) 
            supported in Streamlit (including the Streamlit-based "Simple Charts"), 
            though we will just mainly be focusing on [Altair-related](https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart) plots 
            and their interactivity options since we'll also be making use of these when 
            we move to building Jekyll webpages.
 """)

st.markdown("""Since `matplotlib` is relatively familiar though, let's do a quick 
            example using `pandas` and `matplotlib` to plot as 
            Streamlit [does support `matplotlib`](https://docs.streamlit.io/develop/api-reference/charts/st.pyplot) 
            as a plotting engine. """)

st.markdown("""First, let's just make a simple plot with `pandas` and `matplotlib`. 
            Let's re-do the matplotlib plots we did before with the mobility dataset 
            with some interactivity. """)

import pandas as pd
import numpy as np

# first, let's make a static plot:
st.write("We'll start with a static plot:")
# read in dataset
df = pd.read_csv("https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/mobility.csv")

# make bins along student-teacher ratio
bins = np.linspace(df['Student_teacher_ratio'].min(),df['Student_teacher_ratio'].max(), 10)

# make pivot table
table = df.pivot_table(index='State', columns=pd.cut(df['Student_teacher_ratio'], bins), aggfunc='size')

# our plotting code before was:
st.code("""
import matplotlib.pyplot as plt

fig,ax = plt.subplots(figsize=(10,8))
ax.imshow(table.values, cmap='hot', interpolation='nearest')
ax.set_yticks(range(len(table.index)))
ax.set_yticklabels(table.index)
plt.show()
 """)

st.write("Let's translate it into something that will work with Streamlit:")

import matplotlib.pyplot as plt

fig,ax = plt.subplots() # this changed
ax.imshow(table.values, cmap='hot', interpolation='nearest')
ax.set_yticks(range(len(table.index)))
ax.set_yticklabels(table.index)

st.pyplot(fig) # this is different

st.markdown("""But this is too big!  The trick is that we can save this as a buffer: """)

from io import BytesIO

fig,ax = plt.subplots(figsize=(4,8)) # this changed
ax.imshow(table.values, cmap='hot', interpolation='nearest')
ax.set_yticks(range(len(table.index)))
ax.set_yticklabels(table.index)

buf = BytesIO()
fig.tight_layout()
fig.savefig(buf, format="png")
st.image(buf, width = 500) # can mess around with width, figsize/etc

st.write("Now, let's make this interactive.")
st.markdown("""We'll first use the [multiselect](https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect) 
            tool in order to allow for multiple state selection. """)

# vertical alignment so they end up side by side
fig_col, controls_col = st.columns([2,1], vertical_alignment='center')

# multi-select
states_selected = controls_col.multiselect('Which states do you want to view?', table.index.values)

if len(states_selected) > 0:
    df_subset = df[df['State'].isin(states_selected)] # changed

    # make pivot table -- changed
    table_sub = df_subset.pivot_table(index='State', 
                                  columns=pd.cut(df_subset['Student_teacher_ratio'], bins), 
                                  aggfunc='size')

    base_size = 4
    # this resizing doesn't 100% work great
    #factor = len(table.index)*1.0/df['State'].nunique()
    #if factor == 0: factor = 1 # for non-selections
    #fig,ax = plt.subplots(figsize=(base_size,2*base_size*factor)) # this changed too for different size
    fig,ax = plt.subplots(figsize=(base_size,2*base_size)) # this changed too for different size
    # extent is (xmin, xmax, ymax (buttom), ymin (top))
    extent = [bins.min(), bins.max(), 0, len(table_sub.index)]
    ax.imshow(table_sub.values, cmap='hot', interpolation='nearest', 
              extent=extent)
    ax.set_yticks(range(len(table_sub.index)))
    ax.set_yticklabels(table_sub.index)
    #ax.set_xticklabels(bins)

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    fig_col.image(buf, width = 400) # changed here to fit better
else:
    fig,ax = plt.subplots(figsize=(4,8)) # this changed
    extent = [bins.min(), bins.max(), 0, len(table.index)]
    ax.imshow(table.values, cmap='hot', interpolation='nearest', extent=extent)
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels(table.index)
    #ax.set_xticklabels(bins)

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    fig_col.image(buf, width = 500) # can mess around with width, figsize/etc


st.markdown(""" 
Now let's add more in by including a [range slider](https://docs.streamlit.io/develop/api-reference/widgets/st.slider) 
            widget.
""")

# vertical alignment so they end up side by side
fig_col2, controls_col2 = st.columns([2,1], vertical_alignment='center')

# multi-select
states_selected2 = controls_col2.multiselect('Which states do you want to view?', 
                                             table.index.values, key='unik1155') 
#                                            had to pass unique key to have double widgets with same value

# range slider -- added
student_teacher_ratio_range = controls_col2.slider("Range of student teacher ratio:", 
                                                   df['Student_teacher_ratio'].min(), 
                                                   df['Student_teacher_ratio'].max(), 
                                                   (0.25*df['Student_teacher_ratio'].mean(), 
                                                    0.75*df['Student_teacher_ratio'].mean()))

# note all the "2's" here, probably will just update the original one
if len(states_selected2) > 0: # here we set a default value for the slider, so no need to have a tag
    min_range = student_teacher_ratio_range[0] # added
    max_range = student_teacher_ratio_range[1] # added

    df_subset2 = df[(df['State'].isin(states_selected2)) & (df['Student_teacher_ratio'] >= min_range) & (df['Student_teacher_ratio']<=max_range)] # changed

    # just 10 bins over the full range --> changed
    bins2 = 10 #np.linspace(df['Student_teacher_ratio'].min(),df['Student_teacher_ratio'].max(), 10)

    # make pivot table -- changed
    table_sub2 = df_subset2.pivot_table(index='State', 
                                  columns=pd.cut(df_subset2['Student_teacher_ratio'], bins2), 
                                  aggfunc='size')

    base_size = 4
    fig2,ax2 = plt.subplots(figsize=(base_size,2*base_size)) # this changed too for different size
    extent2 = [df_subset2['Student_teacher_ratio'].min(), 
               df_subset2['Student_teacher_ratio'].max(), 
               0, len(table_sub2.index)]
    ax2.imshow(table_sub2.values, cmap='hot', interpolation='nearest', extent=extent2)
    ax2.set_yticks(range(len(table_sub2.index)))
    ax2.set_yticklabels(table_sub2.index)
    #ax2.set_xticklabels()

    buf2 = BytesIO()
    fig2.tight_layout()
    fig2.savefig(buf2, format="png")
    fig_col2.image(buf2, width = 400) # changed here to fit better
else:
    min_range = student_teacher_ratio_range[0] # added
    max_range = student_teacher_ratio_range[1] # added

    df_subset2 = df[(df['Student_teacher_ratio'] >= min_range) & (df['Student_teacher_ratio']<=max_range)] # changed

    # just 10 bins over the full range --> changed
    bins2 = 10 #np.linspace(df['Student_teacher_ratio'].min(),df['Student_teacher_ratio'].max(), 10)

    # make pivot table -- changed
    table_sub2 = df_subset2.pivot_table(index='State', 
                                  columns=pd.cut(df_subset2['Student_teacher_ratio'], bins2), 
                                  aggfunc='size')

    base_size = 4
    fig2,ax2 = plt.subplots(figsize=(base_size,2*base_size)) # this changed too for different size
    extent2 = [df_subset2['Student_teacher_ratio'].min(), 
               df_subset2['Student_teacher_ratio'].max(), 
               0, len(table_sub2.index)]
    ax2.imshow(table_sub2.values, cmap='hot', interpolation='nearest', extent=extent2)
    ax2.set_yticks(range(len(table_sub2.index)))
    ax2.set_yticklabels(table_sub2.index)
    #ax2.set_xticklabels()

    buf2 = BytesIO()
    fig2.tight_layout()
    fig2.savefig(buf2, format="png")
    fig_col2.image(buf2, width = 400) # changed here to fit better

st.header('Push final page to HF')
st.markdown("""When ready, do:""")
st.code("""
git add -A
git commit -m "final push of day 1"
git push
 """)