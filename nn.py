import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import streamlit.components.v1 as components
import time

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="박민수의 프로필 발표",
    page_icon="👨‍💻",
    layout="wide"
)

# --- 스타일(CSS) 통합 관리 ---
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    
    <style>
        html, body, [class*="st-"], .st-emotion-cache-1kyxreq e1fb0mya1 { font-family: 'Noto Sans KR', sans-serif !important; }
        .slide-container-mbti { width: 100%; min-height: 720px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; overflow: hidden; border-radius: 15px; padding: 2rem; box-sizing: border-box; }
        .floating-shapes { position: absolute; width: 100%; height: 100%; top:0; left:0; pointer-events: none; }
        .shape { position: absolute; border-radius: 50%; background: rgba(255, 255, 255, 0.08); animation: float 8s ease-in-out infinite; }
        .shape:nth-child(1) { width: 100px; height: 100px; top: 5%; left: 5%; animation-delay: 0s; }
        .shape:nth-child(2) { width: 150px; height: 150px; top: 15%; right: 10%; animation-delay: 3s; }
        .shape:nth-child(3) { width: 80px; height: 80px; bottom: 15%; left: 15%; animation-delay: 6s; }
        @keyframes float { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-30px) rotate(180deg); } }
        .mbti-content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; transform: translateY(30px); opacity: 0; animation: slideUp 0.8s ease-out forwards; display: flex; flex-direction: column; }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .intj-title { font-weight: 700; font-size: 4.5rem; text-align: center; margin-bottom: 1.5rem; animation: titlePulse 5s ease-in-out infinite; text-shadow: 2px 2px 8px rgba(30, 27, 46, 0.5); }
        @keyframes titlePulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        .keyword-badge { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.75rem 1.5rem; border-radius: 25px; font-weight: 600; margin: 0.5rem; display: inline-flex; align-items: center; box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3); transition: all 0.3s ease; animation: bounceIn 0.6s ease-out; }
        .keyword-badge:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 8px 25px rgba(255, 154, 158, 0.4); }
        @keyframes bounceIn { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 1; } }
        .mbti-component { background: linear-gradient(135deg, #a8edea, #fed6e3); padding: 1rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3); transition: all 0.3s ease; height:100%; }
        .mbti-component:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(168, 237, 234, 0.4); }
        .mbti-letter { font-size: 2.5rem; font-weight: 900; color: #4a5568; margin-bottom: 0.5rem; }
        .comparison-table { background: rgba(255, 255, 255, 0.9); border-radius: 15px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); height: 100%; }
        .table-header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1rem; font-weight: 700; text-align: center; }
        .table-content { padding: 1.5rem; }
        .strength-item, .development-item { display: flex; align-items: center; margin-bottom: 0.75rem; padding: 0.5rem; border-radius: 8px; transition: all 0.3s ease; }
        .strength-item:hover { background: rgba(102, 126, 234, 0.1); }
        .development-item:hover { background: rgba(255, 154, 158, 0.1); }
        .field-badge { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #444; padding: 0.75rem 1.25rem; border-radius: 20px; font-weight: 600; margin: 0.25rem; display: inline-block; box-shadow: 0 3px 12px rgba(132, 250, 176, 0.3); transition: all 0.3s ease; }
        .field-badge:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(132, 250, 176, 0.4); }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
    </style>
""", unsafe_allow_html=True)

# --- HTML 콘텐츠 정의 ---

# 2번 슬라이드 (MBTI)
mbti_slide_body_html = """
<div class="slide-container-mbti">
    <div class="floating-shapes">
        <div class="shape"></div> <div class="shape"></div> <div class="shape"></div>
    </div>
    <div class="relative z-10">
        <h1 class="intj-title" style="color: white;">INTJ</h1>
        <div class="mbti-content-card p-6 mb-6">
            <h2 class="section-title"><div class="icon-container"><i class="fas fa-star"></i></div>핵심 키워드</h2>
            <div class="text-center">
                <div class="keyword-badge"><i class="fas fa-lightbulb mr-2"></i>논리적</div>
                <div class="keyword-badge"><i class="fas fa-chart-line mr-2"></i>전략적</div>
                <div class="keyword-badge"><i class="fas fa-brain mr-2"></i>분석적</div>
                <div class="keyword-badge"><i class="fas fa-bullseye mr-2"></i>목표지향적</div>
                <div class="keyword-badge"><i class="fas fa-tools mr-2"></i>독창적</div>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="mbti-content-card p-6">
                <h2 class="section-title"><div class="icon-container"><i class="fas fa-puzzle-piece"></i></div>구성요소</h2>
                <div class="grid grid-cols-2 gap-3">
                    <div class="mbti-component"><div class="mbti-letter">I</div><div class="text-sm font-semibold">내향형</div></div>
                    <div class="mbti-component"><div class="mbti-letter">N</div><div class="text-sm font-semibold">직관형</div></div>
                    <div class="mbti-component"><div class="mbti-letter">T</div><div class="text-sm font-semibold">사고형</div></div>
                    <div class="mbti-component"><div class="mbti-letter">J</div><div class="text-sm font-semibold">판단형</div></div>
                </div>
            </div>
            <div class="mbti-content-card p-0">
                <div class="comparison-table">
                    <div class="table-header"><i class="fas fa-balance-scale mr-2"></i>강점 & 발전영역</div>
                    <div class="table-content">
                        <div class="mb-4">
                            <h4 class="font-bold text-green-600 mb-2"><i class="fas fa-thumbs-up mr-1"></i>주요 강점</h4>
                            <div class="strength-item"><i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-sm">높은 독립성</span></div>
                            <div class="strength-item"><i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-sm">분석적 사고</span></div>
                            <div class="strength-item"><i class="fas fa-check-circle text-green-500 mr-2"></i><span class="text-sm">문제 해결 능력</span></div>
                        </div>
                        <div>
                            <h4 class="font-bold text-orange-600 mb-2"><i class="fas fa-arrow-up mr-1"></i>발전 영역</h4>
                            <div class="development-item"><i class="fas fa-exclamation-triangle text-orange-500 mr-2"></i><span class="text-sm">감정 표현</span></div>
                            <div class="development-item"><i class="fas fa-exclamation-triangle text-orange-500 mr-2"></i><span class="text-sm">사회적 교류</span></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mbti-content-card p-6">
                <h2 class="section-title"><div class="icon-container"><i class="fas fa-code"></i></div>적합한 개발 분야</h2>
                <div class="grid grid-cols-1 gap-3 flex-grow">
                    <div class="field-badge text-center block"><i class="fas fa-database mr-2"></i>데이터 과학/AI</div>
                    <div class="field-badge text-center block"><i class="fas fa-sitemap mr-2"></i>시스템 설계</div>
                    <div class="field-badge text-center block"><i class="fas fa-server mr-2"></i>백엔드 개발</div>
                    <div class="field-badge text-center block"><i class="fas fa-cogs mr-2"></i>알고리즘 최적화</div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# (이후 코드는 모두 동일합니다)
# 3번 슬라이드 (직업가치관)
job_values_html = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>직업가치관 검사</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; min-height: 950px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; overflow: hidden; padding: 2rem; box-sizing: border-box; border-radius: 15px; }
        .floating-shapes { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; }
        .shape { position: absolute; border-radius: 50%; background: rgba(255, 255, 255, 0.08); animation: float 8s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-25px); } }
        .main-title { color: #e9e7f5; font-weight: 700; font-size: 3rem; text-align: center; margin-bottom: 1.5rem; animation: titlePulse 5s ease-in-out infinite; text-shadow: 2px 2px 8px rgba(30, 27, 46, 0.5); }
        @keyframes titlePulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        .content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; transform: translateY(30px); opacity: 0; animation: slideUp 0.8s ease-out forwards; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .main-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
        .chart-container { height: 350px; position: relative; }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
        .value-item { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; margin-bottom: 0.5rem; border-radius: 10px; transition: all 0.3s ease; font-size: 0.9rem; }
        .top-value { background: linear-gradient(135deg, #10b981, #059669); color: white; animation: slideInRight 0.6s ease-out; }
        .bottom-value { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; animation: slideInRight 0.6s ease-out; }
        @keyframes slideInRight { from { transform: translateX(30px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .value-item:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); }
        .score-badge { background: rgba(255, 255, 255, 0.3); padding: 0.25rem 0.75rem; border-radius: 15px; font-weight: 700; font-size: 0.85rem; }
        .job-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .job-badge { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #374151; padding: 0.5rem 0.75rem; border-radius: 15px; font-weight: 600; font-size: 0.8rem; text-align: center; box-shadow: 0 3px 12px rgba(132, 250, 176, 0.3); transition: all 0.3s ease; animation: bounceIn 0.6s ease-out; }
        .job-badge:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 6px 20px rgba(132, 250, 176, 0.4); }
        @keyframes bounceIn { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 1; } }
        .insights-section { grid-column: 1 / -1; padding: 1.5rem; text-align: center; }
        .insight-text { color: #4a5568; font-size: 1rem; line-height: 1.6; margin-bottom: 1rem; }
        .highlight { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.25rem 0.5rem; border-radius: 8px; font-weight: 600; }
    </style>
    </head><body>
    <div class="slide-container">
        <div class="floating-shapes"><div class="shape"></div><div class="shape"></div><div class="shape"></div></div>
        <div class="relative z-10">
            <h1 class="main-title">직업가치관 검사 결과</h1>
            <div class="main-grid">
                <div class="content-card p-6">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-chart-area"></i></div>가치관 분석 차트</h2>
                    <div class="chart-container"><canvas id="valueChart"></canvas></div>
                </div>
                <div class="space-y-4">
                    <div class="content-card p-4">
                        <h2 class="section-title"><div class="icon-container"><i class="fas fa-trophy"></i></div>상위 가치관</h2>
                        <div class="top-value value-item"><span><i class="fas fa-medal mr-2"></i>경제적 보상</span><span class="score-badge">5.0</span></div>
                        <div class="top-value value-item"><span><i class="fas fa-target mr-2"></i>성취</span><span class="score-badge">4.7</span></div>
                        <div class="top-value value-item"><span><i class="fas fa-shield-alt mr-2"></i>직업안정</span><span class="score-badge">4.6</span></div>
                    </div>
                    <div class="content-card p-4">
                        <h2 class="section-title"><div class="icon-container"><i class="fas fa-arrow-down"></i></div>하위 가치관</h2>
                        <div class="bottom-value value-item"><span><i class="fas fa-hand-holding-heart mr-2"></i>사회적 공헌</span><span class="score-badge">2.2</span></div>
                        <div class="bottom-value value-item"><span><i class="fas fa-thumbs-up mr-2"></i>사회적 인정</span><span class="score-badge">2.7</span></div>
                        <div class="bottom-value value-item"><span><i class="fas fa-sync-alt mr-2"></i>변화지향</span><span class="score-badge">3.2</span></div>
                    </div>
                </div>
            </div>
            <div class="content-card insights-section mt-6">
                <h2 class="section-title justify-center"><div class="icon-container"><i class="fas fa-briefcase"></i></div>추천 직업 분야</h2>
                <div class="job-grid">
                    <div class="job-badge"><i class="fas fa-shield-alt mr-1"></i>산업안전원</div>
                    <div class="job-badge"><i class="fas fa-flask mr-1"></i>자연과학연구원</div>
                    <div class="job-badge"><i class="fas fa-balance-scale mr-1"></i>법무사</div>
                    <div class="job-badge"><i class="fas fa-user-tie mr-1"></i>정부행정관리자</div>
                    <div class="job-badge"><i class="fas fa-microscope mr-1"></i>환경시험원</div>
                    <div class="job-badge"><i class="fas fa-map mr-1"></i>GIS전문가</div>
                </div>
                <div class="insight-text mt-4">
                    <span class="highlight">경제적 보상</span>과 <span class="highlight">성취</span>를 중시하며, <span class="highlight">안정적인 직업환경</span>을 선호합니다.
                </div>
            </div>
        </div>
    </div>
    <script>
        const ctx = document.getElementById('valueChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['경제적 보상', '성취', '직업안정', '자기개발', '일과 삶의 균형', '자율성', '변화지향', '사회적 인정', '사회적 공헌'],
                datasets: [{
                    label: '직업가치관 점수', data: [5.0, 4.7, 4.6, 4.2, 4.0, 3.8, 3.2, 2.7, 2.2],
                    backgroundColor: 'rgba(102, 126, 234, 0.2)', borderColor: 'rgba(102, 126, 234, 1)', borderWidth: 3,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)', pointBorderColor: '#fff', pointBorderWidth: 2, pointRadius: 6, pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
                scales: {
                    r: {
                        beginAtZero: true, max: 5,
                        ticks: { stepSize: 1, font: { size: 12, family: 'Noto Sans KR' }, color: '#6b7280' },
                        pointLabels: { font: { size: 11, family: 'Noto Sans KR', weight: '600' }, color: '#374151' },
                        grid: { color: 'rgba(107, 114, 128, 0.3)' }, angleLines: { color: 'rgba(107, 114, 128, 0.3)' }
                    }
                },
                animation: { duration: 2000, easing: 'easeInOutQuart' }
            }
        });
    </script></body></html>
"""

# 4번 슬라이드 (직무역량)
competency_html = """
<!DOCTYPE html><html lang="ko"><head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>직무역량 분석</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { font-family: 'Noto Sans KR', sans-serif; }
        .slide-container { width: 100%; min-height: 950px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; overflow: hidden; padding: 2rem; box-sizing: border-box; border-radius: 15px; }
        .floating-shapes { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; }
        .shape { position: absolute; border-radius: 50%; background: rgba(255, 255, 255, 0.08); animation: float 8s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-30px); } }
        .main-title { color: #e9e7f5; font-weight: 700; font-size: 3rem; text-align: center; margin-bottom: 1.5rem; animation: titlePulse 5s ease-in-out infinite; text-shadow: 2px 2px 8px rgba(30, 27, 46, 0.5); }
        @keyframes titlePulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        .content-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 20px; transform: translateY(30px); opacity: 0; animation: slideUp 0.8s ease-out forwards; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); }
        @keyframes slideUp { to { transform: translateY(0); opacity: 1; } }
        .main-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
        .chart-container { height: 300px; position: relative; }
        .section-title { color: #4a5568; font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; }
        .icon-container { background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem; }
        .competency-item { display: flex; align-items: center; margin-bottom: 0.75rem; padding: 0.75rem; border-radius: 10px; transition: all 0.3s ease; font-size: 0.9rem; }
        .strength-item { background: linear-gradient(135deg, #10b981, #059669); color: white; animation: slideInRight 0.6s ease-out; }
        .development-item { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; animation: slideInRight 0.6s ease-out; }
        @keyframes slideInRight { from { transform: translateX(30px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .competency-item:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); }
        .score-badge { background: rgba(255, 255, 255, 0.3); padding: 0.25rem 0.75rem; border-radius: 15px; font-weight: 700; font-size: 0.85rem; margin-left: auto; }
        .insights-section { grid-column: 1 / -1; padding: 1.5rem; text-align: center; }
        .insight-text { color: #4a5568; font-size: 1rem; line-height: 1.6; margin-bottom: 1rem; }
        .highlight { background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #444; padding: 0.25rem 0.5rem; border-radius: 8px; font-weight: 600; }
        .competency-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .competency-badge { background: linear-gradient(135deg, #84fab0, #8fd3f4); color: #374151; padding: 0.5rem 1rem; border-radius: 15px; font-weight: 600; font-size: 0.85rem; text-align: center; box-shadow: 0 3px 12px rgba(132, 250, 176, 0.3); transition: all 0.3s ease; animation: bounceIn 0.6s ease-out; }
        .competency-badge:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 6px 20px rgba(132, 250, 176, 0.4); }
        @keyframes bounceIn { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 1; } }
    </style>
    </head><body>
    <div class="slide-container">
        <div class="floating-shapes"><div class="shape"></div><div class="shape"></div><div class="shape"></div></div>
        <div class="relative z-10">
            <h1 class="main-title">직무역량 분석</h1>
            <div class="main-grid">
                <div class="content-card p-6">
                    <h2 class="section-title"><div class="icon-container"><i class="fas fa-chart-radar"></i></div>역량 분포 차트</h2>
                    <div class="chart-container"><canvas id="competencyChart"></canvas></div>
                </div>
                <div class="space-y-4">
                    <div class="content-card p-4">
                        <h2 class="section-title"><div class="icon-container"><i class="fas fa-star"></i></div>핵심 강점</h2>
                        <div class="strength-item competency-item"><i class="fas fa-brain mr-2"></i><span>논리적 사고력</span><span class="score-badge">95</span></div>
                        <div class="strength-item competency-item"><i class="fas fa-lightbulb mr-2"></i><span>창의적 문제해결</span><span class="score-badge">90</span></div>
                        <div class="strength-item competency-item"><i class="fas fa-bullseye mr-2"></i><span>목표 달성 의지</span><span class="score-badge">85</span></div>
                    </div>
                    <div class="content-card p-4">
                        <h2 class="section-title"><div class="icon-container"><i class="fas fa-arrow-up"></i></div>보완 영역</h2>
                        <div class="development-item competency-item"><i class="fas fa-users mr-2"></i><span>팀워크 및 협업</span><span class="score-badge">60</span></div>
                        <div class="development-item competency-item"><i class="fas fa-heart mr-2"></i><span>감정적 안정성</span><span class="score-badge">55</span></div>
                    </div>
                </div>
            </div>
            <div class="content-card insights-section mt-6">
                <h2 class="section-title justify-center"><div class="icon-container"><i class="fas fa-chart-line"></i></div>종합 분석 및 발전 방향</h2>
                <div class="competency-grid">
                    <div class="competency-badge"><i class="fas fa-cogs mr-2"></i>복잡한 문제 해결</div>
                    <div class="competency-badge"><i class="fas fa-project-diagram mr-2"></i>시스템적 사고</div>
                    <div class="competency-badge"><i class="fas fa-handshake mr-2"></i>소통 역량 개발</div>
                    <div class="competency-badge"><i class="fas fa-balance-scale mr-2"></i>감정 관리 기술</div>
                </div>
                <div class="insight-text mt-4">
                    <span class="highlight">분석적 사고</span>와 <span class="highlight">창의적 문제해결</span>이 뛰어난 개발자형 인재로,
                    <span class="highlight">협업 능력</span>과 <span class="highlight">감정 관리</span> 스킬을 보완하여 팀의 시너지를 극대화할 수 있습니다.
                </div>
            </div>
        </div>
    </div>
    <script>
        const ctx = document.getElementById('competencyChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['논리력', '목표지향성', '창의성', '책임감', '협업능력', '감정적 안정성'],
                datasets: [{
                    label: '직무역량 점수', data: [95, 85, 90, 80, 60, 55],
                    backgroundColor: 'rgba(255, 154, 158, 0.2)', borderColor: 'rgba(255, 154, 158, 1)', borderWidth: 3,
                    pointBackgroundColor: 'rgba(255, 154, 158, 1)', pointBorderColor: '#fff', pointBorderWidth: 2, pointRadius: 6, pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
                scales: {
                    r: {
                        beginAtZero: true, max: 100,
                        ticks: { stepSize: 20, font: { size: 12, family: 'Noto Sans KR' }, color: '#6b7280' },
                        pointLabels: { font: { size: 12, family: 'Noto Sans KR', weight: '600' }, color: '#374151' },
                        grid: { color: 'rgba(107, 114, 128, 0.3)' }, angleLines: { color: 'rgba(107, 114, 128, 0.3)' }
                    }
                },
                animation: { duration: 2000, easing: 'easeInOutQuart' }
            }
        });
    </script></body></html>
"""

# --- 슬라이드 전체 목차 및 내용 정의 ---
slides = {
    "1. 기본 소개": """
        ### 👤 기본 정보
        - **이름:** 박민수
        - **학번:** 23683013
        - **출생지:** 충청남도 공주시
        - **학력:** 공주영명고등학교 졸업, 건양대학교(논산) 재학 중
        ---
        ### 🧾 자격증
        - 한국사능력검정시험 1급
        - 위험물기능사
        ---
        ### 🧩 취미 & 여가생활
        - 영화 감상 (판타지 & SF 장르)
        - 그림 그리기
        - 클라이밍
    """,
    "2. 성격유형(MBTI)": mbti_slide_body_html,
    "3. 직업가치관 검사": "직업가치관검사 결과 내용으로 대체될 영역",
    "4. 직무역량 분석": "이 영역은 아래에서 Streamlit 코드로 직접 렌더링 됩니다."
}


# --- 사이드바 내비게이션 ---
st.sidebar.title("📑 발표 목차")
page_options = ["🏠 홈"] + list(slides.keys())
selected_page = st.sidebar.radio("이동할 페이지를 선택하세요:", page_options)


# --- 메인 화면 페이지 렌더링 ---
if selected_page == "🏠 홈":
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-top: 15vh;'>프로필 발표</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5rem; color: grey;'>저에 대해 소개하는 발표입니다.</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='position: fixed; bottom: 30px; right: 30px; text-align: right; font-size: 1.1rem;'>
            <b>학번:</b> 23683013<br>
            <b>이름:</b> 박민수
        </div>
        """,
        unsafe_allow_html=True
    )

elif selected_page == "1. 기본 소개":
    st.header(selected_page)
    st.markdown("---")
    st.markdown(slides[selected_page], unsafe_allow_html=True)

elif selected_page == "2. 성격유형(MBTI)":
    st.markdown(slides[selected_page], unsafe_allow_html=True)

elif selected_page == "3. 직업가치관 검사":
    components.html(job_values_html, height=1000, scrolling=False)

elif selected_page == "4. 직무역량 분석":
    components.html(competency_html, height=1000, scrolling=False)