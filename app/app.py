# Load penguins data
df = palmerpenguins.load_penguins()

# Set page options
ui.page_opts(title="Julia's Penguin Dashboard", fillable=True)

# Create sidebar with filters
with ui.sidebar(title="Filter Penguins by Mass and Species", style="background-color: lightblue;"):
    # Slider for mass filtering
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Checkbox group for species filtering
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Useful links section
    ui.hr()  # Horizontal line for separation
    ui.h6("Links")  # Header for links
    # Links to GitHub, PyShiny, and other resources
    ui.a(
        "GitHub Source",
        href="https://github.com/julia-fangman/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://julia-fangman.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/julia-fangman/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Create Value boxes for data
with ui.layout_column_wrap(fill=False):
    # Value box for total number of penguins
    with ui.value_box(showcase=icon_svg("earlybirds"), style="background-color: yellow;"):
        "Number of penguins"
        # Display total number of penguins
        @render.text
        def count():
            return filtered_df().shape[0]

    # Value box for average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="background-color: yellow;"):
        "Average bill length"
        # Display average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box for average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="background-color: yellow;"):
        "Average bill depth"
        # Display average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    # Card for histogram of bill length vs. bill depth
    with ui.card(full_screen=True, style="background-color: pink;"):
        ui.card_header("Bill Length vs. Bill Depth")
        # Render Plotly histogram
        @render_plotly
        def length_depth_plotly():
            return px.histogram(
                data_frame=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
            )

    # Card for penguin data summary
    with ui.card(full_screen=True, style="background-color: pink;"):
        ui.card_header("Penguin Data")
        # Display penguin data in a DataGrid
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Define reactive function to filter data frame
@reactive.calc
def filtered_df():
    # Filter dataframe based on selected species and mass range
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
