import pandas as pd
import plotly.express as px

CSV_FILE = "mood_log.csv"

def plot_mood_last_7_days(csv_path=CSV_FILE):
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            fig = px.line(title="暂无情绪数据，快去记录第一条吧~ 🌱")
            fig.update_layout(yaxis_range=[0.5, 5.5])
            return fig

        df["日期"] = pd.to_datetime(df["日期"])
        df = df.sort_values("日期")
        df_last7 = df.tail(7)

        fig = px.line(
            df_last7,
            x="日期",
            y="心情分数",
            markers=True,
            title="📊 最近7天情绪趋势",
            line_shape="spline",
            range_y=[0.5, 5.5]
        )
        fig.update_layout(
            yaxis_title="心情分数",
            xaxis_title="日期",
            hovermode="x unified",
            font=dict(size=14)
        )

        min_score = df_last7["心情分数"].min()
        max_score = df_last7["心情分数"].max()
        fig.add_hline(y=min_score, line_dash="dot", line_color="gray",
                      annotation_text=f"最低 {min_score} 分")
        fig.add_hline(y=max_score, line_dash="dot", line_color="green",
                      annotation_text=f"最高 {max_score} 分")
        return fig

    except FileNotFoundError:
        fig = px.line(title="还没有情绪记录哦，先去记录吧~ 🌿")
        fig.update_layout(yaxis_range=[0.5, 5.5])
        return fig
    except Exception as e:
        fig = px.line(title=f"图表生成失败：{e}")
        return fig

if __name__ == "__main__":
    fig = plot_mood_last_7_days()
    fig.show()