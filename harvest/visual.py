import streamlit as st
import plotly.graph_objs as go


class Visual:
    CONFIG = {"displayModeBar": False}

    def __int__(self):
        pass

    def plotly_piechart(self, data, title, labels, values, colormap):
        colors = [colormap.get(label, "#CCCCCC") for label in data[labels].values]

        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=data[labels].values,
                values=data[values].values,
                hole=0.3,
                texttemplate="%{percent:.2%}",
                textfont=dict(size=18),
                hovertemplate="%{label}: %{value} hours <extra></extra>",
                marker=dict(colors=colors)
            )
        )

        fig.update_layout(
            title_text=title,
            height=500,
            hoverlabel=dict(font_size=16)
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)

    def plotly_barchart(self, title, data, labels, values, orientation="v"):
        fig = go.Figure()

        x = data[labels] if orientation == "v" else data[values]
        y = data[values] if orientation == "v" else data[labels]
        text = y if orientation == "v" else x
        hovertemplate = "%{x}: %{y} hours" if orientation == "v" else "%{y}: %{x} hours"

        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                text=text,
                texttemplate="%{text:.2f}",
                textfont=dict(size=18),
                orientation=orientation,
                hovertemplate=hovertemplate + " <extra></extra>",
                marker=dict(color="#94D2BD")
            )
        )

        fig.update_layout(
            title_text=title,
            height=500,
            xaxis=dict(
                title=dict(text=labels, font=dict(size=16)),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                title=dict(text=values, font=dict(size=16)),
                tickfont=dict(size=14)
            )
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)

    def plotly_stackbar(self, title, data, labels, values, orientation="v", barmode="stack", breakdown=None):
        default_colormap = {
            "Yes": "#0A9396",
            "No": "#BB3E03"
        }

        fig = go.Figure()

        categories = data[breakdown].unique()
        for category in categories:
            subset = data[data[breakdown] == category]
            x = subset[labels] if orientation == "v" else subset[values]
            y = subset[values] if orientation == "v" else subset[labels]
            text = y if orientation == "v" else x
            hovertemplate = "%{x}: %{y} hours" if orientation == "v" else "%{y}: %{x} hours"

            color = default_colormap.get(category, "#CCCCCC")

            fig.add_trace(
                go.Bar(
                    name=category,
                    x=x,
                    y=y,
                    text=text,
                    texttemplate="%{text:.2%}",
                    textfont=dict(size=18),
                    orientation=orientation,
                    hovertemplate=hovertemplate + " <extra></extra>",
                    marker=dict(color=color)
                )
            )

        fig.update_layout(
            title_text=title,
            height=500,
            xaxis=dict(
                title=dict(text=labels, font=dict(size=16)),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                title=dict(text=values, font=dict(size=16)),
                tickfont=dict(size=14)
            ),
            barmode=barmode
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)
