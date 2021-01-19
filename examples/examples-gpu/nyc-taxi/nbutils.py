from IPython.core.display import HTML

def style():
    return HTML("""
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">    
<style>
.nbhero{
    background-image: url("https://www.saturncloud.io/s/wp-content/uploads/2020/07/scalability.jpg");
    height: 500px;
    width: 100%;
    font-family: 'Lato', sans-serif;
    text-align: center;
    color: white;
}
.nb.title{
    font-size: 3em;
    padding-top: 3em;
}
.nb.subtitle{
    font-size: 2em;
    padding-top: 1em;
}
.nb.description{
    font-size: 1.5em;
    padding-top: 1em;
}
a.nb.link{
    color: lightblue;
}
</style>
""")