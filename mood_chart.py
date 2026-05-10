import pandas as pd
import plotly.express as px
import os


def plot_mood_last_7_days(user_id="default"):
    """
    读取指定用户的情绪日志，生成最近7天的情绪趋势折线图。
    
    参数:
        user_id: 用户唯一标识（可选，默认 "default"）
    
    返回:
        plotly.graph_objects.Figure 对象
    """
    csv_file = f"mood_log_{user_id}.csv"
    
    try:
        if not os.path.exists(csv_file):
            fig = px.line(title="📊 最近7天情绪趋势｜还没有记录哦，先去记录吧~ 🌿")
            fig.update_layout(yaxis_range=[0.5, 5.5])
            return fig

        df = pd.read_csv(csv_file)
        if df.empty:
            fig = px.line(title="📊 最近7天情绪趋势｜还没有记录哦")
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
            range_y=[0.5, 5.5],
        )
        fig.update_layout(
            yaxis_title="心情分数",
            xaxis_title="日期",
            hovermode="x unified",
            font=dict(size=14),
        )

        if "心情分数" in df_last7.columns and not df_last7["心情分数"].empty:
            min_score = df_last7["心情分数"].min()
            max_score = df_last7["心情分数"].max()
            fig.add_hline(y=min_score, line_dash="dot", line_color="gray",
                          annotation_text=f"最低 {min_score} 分")
            fig.add_hline(y=max_score, line_dash="dot", line_color="green",
                          annotation_text=f"最高 {max_score} 分")
        return fig

    except Exception as e:
        fig = px.line(title=f"图表生成失败：{e}")
        return fig


if __name__ == "__main__":
    fig = plot_mood_last_7_days(user_id="test_user")
    fig.show()