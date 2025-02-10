import streamlit as st
import plotly.graph_objs as go


class Visual:
    CONFIG = {"displayModeBar": False}

    def __int__(self):
        pass

    def plotly_piechart(self, data, title, labels, values):
        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=data[labels].values,
                values=data[values].values,
                hole=0.3,
                texttemplate="%{percent:.2%}",
                hovertemplate="%{label}: %{value} hours <extra></extra>"
            )
        )

        fig.update_layout(
            title_text=title,
            height=500
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
                orientation=orientation,
                hovertemplate=hovertemplate + " <extra></extra>"
            )
        )

        fig.update_layout(
            title_text=title,
            height=500
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)

    def plotly_stackbar(self, title, data, labels, values, orientation="v", barmode="stack", breakdown=None):
        fig = go.Figure()

        categories = data[breakdown].unique()
        for category in categories:
            subset = data[data[breakdown] == category]
            x = subset[labels] if orientation == "v" else subset[values]
            y = subset[values] if orientation == "v" else subset[labels]
            text = y if orientation == "v" else x
            hovertemplate = "%{x}: %{y} hours" if orientation == "v" else "%{y}: %{x} hours"

            fig.add_trace(
                go.Bar(
                    name=category,
                    x=x,
                    y=y,
                    text=text,
                    texttemplate="%{text:.2f}",
                    orientation=orientation,
                    hovertemplate=hovertemplate + " <extra></extra>"
                )
            )

        fig.update_layout(
            title_text=title,
            height=500,
            barmode=barmode
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)
