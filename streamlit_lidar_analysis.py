import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="라이다 센서 분석",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 제목
st.title("🚗 자율주행 라이다 센서 분석")
st.markdown("### 무리함수와 아폴로니우스 원의 응용")

# 사이드바 설정
st.sidebar.markdown("## ⚙️ 설정")
k_a = st.sidebar.slider("센서 A 오차 상수 (k_A)", 0.1, 1.0, 0.5, 0.1)
k_b = st.sidebar.slider("센서 B 오차 상수 (k_B)", 0.1, 1.0, 0.6, 0.1)
max_distance = st.sidebar.slider("최대 분석 거리 (m)", 20, 50, 30, 5)

# 탭 구성
# 수정: 6개 탭
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 무리함수 오차",
    "⭕ 아폴로니우스 원",
    "🔄 복합 분석",
    "🎯 신뢰도 맵",
    "📊 시뮬레이션",
    "📘 자료 분석 가이드"
])


# ==================== TAB 1: 무리함수 오차 ====================
with tab1:
    st.header("1. 라이다 거리 오차의 무리함수 모델")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📐 이론")
        st.write("""
        라이다 센서의 거리 측정 오차는 거리에 따라 증가합니다:
        
        **공식**: σ(r) = k√r
        
        - k: 센서 특성 상수
        - r: 거리 (m)
        - σ: 오차 (m)
        
        **특징**:
        - 무리함수는 항상 증가
        - 증가 속도는 점점 감소
        - 미분: dσ/dr = k/(2√r)
        """)
    
    with col2:
        st.subheader("📊 그래프")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # 거리-오차 그래프
        r = np.linspace(0.1, max_distance, 1000)
        
        sigma_a = k_a * np.sqrt(r)
        sigma_b = k_b * np.sqrt(r)
        
        ax1.plot(r, sigma_a, 'b-', linewidth=2, label=f'센서 A (k={k_a})')
        ax1.plot(r, sigma_b, 'r-', linewidth=2, label=f'센서 B (k={k_b})')
        ax1.fill_between(r, sigma_a, alpha=0.2, color='blue')
        ax1.fill_between(r, sigma_b, alpha=0.2, color='red')
        ax1.set_xlabel('거리 r (m)', fontsize=12)
        ax1.set_ylabel('오차 σ (m)', fontsize=12)
        ax1.set_title('무리함수: σ(r) = k√r', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=11)
        
        # 미분 (변화율) 그래프
        derivative_a = k_a / (2 * np.sqrt(r))
        derivative_b = k_b / (2 * np.sqrt(r))
        
        ax2.plot(r, derivative_a, 'b-', linewidth=2, label=f'dσ_A/dr')
        ax2.plot(r, derivative_b, 'r-', linewidth=2, label=f'dσ_B/dr')
        ax2.set_xlabel('거리 r (m)', fontsize=12)
        ax2.set_ylabel('오차 변화율 (m/m)', fontsize=12)
        ax2.set_title('미분: dσ/dr = k/(2√r)', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=11)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # 수치 테이블
    st.subheader("📋 거리별 오차 계산표")
    distances = np.array([5, 10, 15, 20, 25, 30])
    error_a = k_a * np.sqrt(distances)
    error_b = k_b * np.sqrt(distances)
    
    df = pd.DataFrame({
        '거리 (m)': distances,
        f'센서 A 오차 (cm)': np.round(error_a * 100, 2),
        f'센서 B 오차 (cm)': np.round(error_b * 100, 2),
        '오차 비율 (B/A)': np.round(error_b / error_a, 3)
    })
    
    st.dataframe(df, use_container_width=True)
    
    # 공식 설명
    st.subheader("🔬 왜 무리함수인가?")
    st.write("""
    **물리적 근거**:
    1. 신호 강도 ∝ 1/r² (역제곱 법칙)
    2. 측정 오차 ∝ √(신호 강도) (샷 노이즈)
    3. 따라서: σ ∝ √(1/r²) = 1/r는 아니고,
       실제로는 센서의 절대 감도 때문에 σ ∝ √r
    """)

# ==================== TAB 2: 아폴로니우스 원 ====================
with tab2:
    st.header("2. 아폴로니우스의 원: 센서 신뢰도 경계")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📐 이론")
        st.write("""
        **아폴로니우스 정리**:
        두 정점까지의 거리 비가 일정한 점들의 자취는 원이다.
        
        수식:
        PA / PB = m / n (m ≠ n, 상수)
        
        **라이다 응용**:
        두 센서의 신뢰도가 같은 점들의 자취
        """)
    
    with col2:
        st.subheader("⭕ 그래프")
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 센서 위치
        sensor_a = np.array([-10.0, 0.0])
        sensor_b = np.array([10.0, 0.0])
        Ax, Ay = sensor_a
        Bx, By = sensor_b
        
        # 센서 신뢰도 비율 (슬라이더로 조정 가능)
        ratio = st.slider("PA/PB 비율", 0.5, 3.0, 1.5, 0.1)
        m = float(ratio)
        
        # 아폴로니우스 원 계산 (일반식)
        if abs(m - 1.0) > 1e-8:
            cx = (Ax - m**2 * Bx) / (1 - m**2)
            cy = (Ay - m**2 * By) / (1 - m**2)
            C = (Ax**2 + Ay**2 - m**2 * (Bx**2 + By**2)) / (1 - m**2)
            r_sq = cx**2 + cy**2 - C
            if r_sq > 0:
                r = np.sqrt(r_sq)
            else:
                r = None
        else:
            cx = None
            cy = None
            r = None
        
        # 센서 그리기
        ax.plot(Ax, Ay, 'bo', markersize=10, label='센서 A (-10, 0)')
        ax.plot(Bx, By, 'ro', markersize=10, label='센서 B (10, 0)')
        
        # 아폴로니우스 원 그리기
        if r is not None:
            circle = Circle((cx, cy), r, fill=False, color='green', linewidth=2.5, linestyle='--', label=f'아폴로니우스 원 (비율={ratio})')
            ax.add_patch(circle)
        else:
            # ratio = 1일 때는 수직이등분선 또는 원이 불가능한 경우
            if abs(m - 1.0) < 1e-8:
                ax.axvline(x=(Ax + Bx) / 2.0, color='green', linewidth=2.5, linestyle='--', label='PA/PB = 1 (수직이등분선)')
            else:
                ax.text(0, 0, '아폴로니우스 원을 계산할 수 없습니다\n(수치적으로 불안정)', ha='center')
        
        # 배경 라이다 범위
        circle_a = Circle((Ax, Ay), 30, fill=False, color='blue', linewidth=1.5, alpha=0.3, linestyle=':')
        circle_b = Circle((Bx, By), 30, fill=False, color='red', linewidth=1.5, alpha=0.3, linestyle=':')
        ax.add_patch(circle_a)
        ax.add_patch(circle_b)
        
        ax.set_xlim(-50, 50)
        ax.set_ylim(-40, 40)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x (m)', fontsize=12)
        ax.set_ylabel('y (m)', fontsize=12)
        ax.set_title(f'아폴로니우스 원: PA/PB = {ratio}', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11, loc='upper right')
        
        plt.tight_layout()
        st.pyplot(fig)

# ==================== TAB 3: 복합 분석 ====================
with tab3:
    st.header("3. 복합 분석: 무리함수 + 아폴로니우스 원")
    
    st.subheader("📊 신뢰도 기반 센서 선택")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("""
        **센서 신뢰도**:
        
        T_A = 1 / (1 + σ_A)
        T_B = 1 / (1 + σ_B)
        
        여기서:
        - σ_A = k_A√(|PA|)
        - σ_B = k_B√(|PB|)
        """)
    
    with col2:
        st.write("""
        **신뢰도 맵 해석**:
        - 🔵 파란색 (진함): 센서 A의 신뢰도 높음
        - 🔴 빨간색 (진함): 센서 B의 신뢰도 높음
        - 🟣 보라색: 비슷한 신뢰도 (경계선)
        """)
    
    # 2D 신뢰도 맵 생성
    x = np.linspace(-40, 40, 400)
    y = np.linspace(-40, 40, 400)
    X, Y = np.meshgrid(x, y)
    
    sensor_a = np.array([-10.0, 0.0])
    sensor_b = np.array([10.0, 0.0])
    Ax, Ay = sensor_a
    Bx, By = sensor_b

    # 거리 계산 (각 축별로 명시)
    dist_a = np.sqrt((X - Ax)**2 + (Y - Ay)**2)
    dist_b = np.sqrt((X - Bx)**2 + (Y - By)**2)

    # 오차 계산 (무리함수)
    sigma_a = k_a * np.sqrt(dist_a + 1e-9)  # 수치 안정성
    sigma_b = k_b * np.sqrt(dist_b + 1e-9)
    
    # 신뢰도 계산
    T_a = 1 / (1 + sigma_a)
    T_b = 1 / (1 + sigma_b)
    
    # 차이 맵 (음수 = A 우수, 양수 = B 우수)
    diff = T_a - T_b
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 센서 A 신뢰도
    im1 = axes[0].contourf(X, Y, T_a, levels=20, cmap='Blues')
    axes[0].plot(Ax, Ay, 'b*', markersize=12)
    axes[0].plot(Bx, By, 'r+', markersize=12, markeredgewidth=2)
    axes[0].set_title('센서 A 신뢰도', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('x (m)')
    axes[0].set_ylabel('y (m)')
    plt.colorbar(im1, ax=axes[0], label='신뢰도')
    
    # 센서 B 신뢰도
    im2 = axes[1].contourf(X, Y, T_b, levels=20, cmap='Reds')
    axes[1].plot(Ax, Ay, 'b*', markersize=12)
    axes[1].plot(Bx, By, 'r+', markersize=12, markeredgewidth=2)
    axes[1].set_title('센서 B 신뢰도', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('x (m)')
    axes[1].set_ylabel('y (m)')
    plt.colorbar(im2, ax=axes[1], label='신뢰도')
    
    # 차이 맵 (경계선 표시)
    im3 = axes[2].contourf(X, Y, diff, levels=20, cmap='RdBu_r')
    axes[2].contour(X, Y, diff, levels=[0], colors='black', linewidths=2)  # 경계선 (T_A == T_B)
    axes[2].plot(Ax, Ay, 'b*', markersize=12, label='센서 A')
    axes[2].plot(Bx, By, 'r+', markersize=12, markeredgewidth=2, label='센서 B')
    axes[2].set_title('신뢰도 차이 (검은선 = 경계)', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('x (m)')
    axes[2].set_ylabel('y (m)')
    axes[2].legend()
    plt.colorbar(im3, ax=axes[2], label='T_A - T_B')
    
    for ax in axes:
        ax.set_xlim(-40, 40)
        ax.set_ylim(-40, 40)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)

# ==================== TAB 4: 신뢰도 맵 ====================
with tab4:
    st.header("4. 상호작용 신뢰도 맵")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎮 설정")
        x_pos = st.slider("마우스 X 위치 (m)", -30, 30, 0, 1)
        y_pos = st.slider("마우스 Y 위치 (m)", -30, 30, 0, 1)
    
    with col2:
        st.subheader("📍 현재 위치에서의 분석")
        
        sensor_a = np.array([-10.0, 0.0])
        sensor_b = np.array([10.0, 0.0])
        pos = np.array([x_pos, y_pos])
        
        dist_a = np.linalg.norm(pos - sensor_a)
        dist_b = np.linalg.norm(pos - sensor_b)
        
        sigma_a = k_a * np.sqrt(dist_a + 1e-9)
        sigma_b = k_b * np.sqrt(dist_b + 1e-9)
        
        T_a = 1 / (1 + sigma_a)
        T_b = 1 / (1 + sigma_b)
        
        # 메트릭 표시
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("센서 A까지 거리", f"{dist_a:.2f} m")
            st.metric("센서 A 오차", f"{sigma_a*100:.2f} cm")
            st.metric("센서 A 신뢰도", f"{T_a*100:.1f}%")
        
        with col_b:
            st.metric("센서 B까지 거리", f"{dist_b:.2f} m")
            st.metric("센서 B 오차", f"{sigma_b*100:.2f} cm")
            st.metric("센서 B 신뢰도", f"{T_b*100:.1f}%")
        
        # 선택 결과
        if T_a > T_b:
            st.success(f"✅ 센서 A 선택 (신뢰도 차이: {(T_a-T_b)*100:.1f}%)", icon="✅")
        elif T_b > T_a:
            st.error(f"✅ 센서 B 선택 (신뢰도 차이: {(T_b-T_a)*100:.1f}%)", icon="🔴")
        else:
            st.info("⚠️ 신뢰도 동일 (경계선 위)", icon="ℹ️")

# ==================== TAB 5: 시뮬레이션 ====================
with tab5:
    st.header("5. 실시간 라이다 데이터 시뮬레이션")
    
    st.subheader("🚗 자동차 이동 시뮬레이션")
    
    # 자동차 경로 설정
    sim_type = st.radio("시뮬레이션 타입", ["직선", "곡선", "원형"]) 
    
    t = np.linspace(0, 2*np.pi, 100)
    
    if sim_type == "직선":
        car_x = np.linspace(-30, 30, 100)
        car_y = np.zeros_like(car_x)
        title = "직선 운동"
    elif sim_type == "곡선":
        car_x = 20 * np.cos(t)
        car_y = 10 * np.sin(t)
        title = "곡선 경로"
    else:  # 원형
        car_x = 20 * np.cos(t)
        car_y = 20 * np.sin(t)
        title = "원형 경로"
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    sensor_a = np.array([-10.0, 0.0])
    sensor_b = np.array([10.0, 0.0])
    Ax, Ay = sensor_a
    Bx, By = sensor_b
    
    # 왼쪽: 경로와 센서
    ax1.plot(car_x, car_y, 'g-', linewidth=2, label='자동차 경로')
    ax1.plot(car_x[0], car_y[0], 'go', markersize=8, label='시작점')
    ax1.plot(car_x[-1], car_y[-1], 'r*', markersize=12, label='종료점')
    
    circle_a = Circle((Ax, Ay), 30, fill=False, color='blue', linewidth=1.5, linestyle=':')
    circle_b = Circle((Bx, By), 30, fill=False, color='red', linewidth=1.5, linestyle=':')
    ax1.add_patch(circle_a)
    ax1.add_patch(circle_b)
    
    ax1.plot(Ax, Ay, 'b*', markersize=12, label='센서 A')
    ax1.plot(Bx, By, 'r*', markersize=12, label='센서 B')
    
    ax1.set_xlim(-40, 40)
    ax1.set_ylim(-40, 40)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_title(f'자동차 경로: {title}', fontsize=12, fontweight='bold')
    ax1.legend()
    
    # 오른쪽: 신뢰도 변화 (거리 계산시 축별로 명시)
    dist_a_arr = np.sqrt((car_x - Ax)**2 + (car_y - Ay)**2)
    dist_b_arr = np.sqrt((car_x - Bx)**2 + (car_y - By)**2)
    
    sigma_a_arr = k_a * np.sqrt(dist_a_arr + 1e-9)
    sigma_b_arr = k_b * np.sqrt(dist_b_arr + 1e-9)
    
    T_a_arr = 1 / (1 + sigma_a_arr)
    T_b_arr = 1 / (1 + sigma_b_arr)
    
    ax2.plot(range(len(car_x)), T_a_arr * 100, 'b-', linewidth=2, label='센서 A 신뢰도')
    ax2.plot(range(len(car_x)), T_b_arr * 100, 'r-', linewidth=2, label='센서 B 신뢰도')
    ax2.fill_between(range(len(car_x)), T_a_arr * 100, alpha=0.2)
    ax2.fill_between(range(len(car_x)), T_b_arr * 100, alpha=0.2)
    
    # 선택 경계
    ax2.axhline(y=50, color='black', linestyle='--', alpha=0.5, label='선택 경계')
    
    ax2.set_xlabel('이동 단계', fontsize=12)
    ax2.set_ylabel('신뢰도 (%)', fontsize=12)
    ax2.set_title('경로 따라 신뢰도 변화', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 통계
    st.subheader("📊 통계 분석")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("센서 A 평균 신뢰도", f"{T_a_arr.mean()*100:.1f}%")
        st.metric("센서 A 선택 횟수", int((T_a_arr > T_b_arr).sum()))
    
    with col2:
        st.metric("센서 B 평균 신뢰도", f"{T_b_arr.mean()*100:.1f}%")
        st.metric("센서 B 선택 횟수", int((T_b_arr > T_a_arr).sum()))
    
    with col3:
        crossover_count = int(np.sum(np.diff((T_a_arr > T_b_arr).astype(int)) != 0))
        st.metric("센서 전환 횟수", crossover_count)

# tab 6----------------------------------------------------------------
with tab6:
    st.header("📘 자료 분석 가이드")
    st.markdown("""

### 1) 핵심 수학 개념 요약
- **유클리드 거리(거리 계산)**  
  임의의 점 $(x,y)$ 와 센서 위치 $(x_0,y_0)$ 사이의 거리:  
  \[
  r = \sqrt{(x-x_0)^2 + (y-y_0)^2}
  \]
  → 격자 전체에 대해 한 번에 계산되며, 거리 값이 그래프의 기본 입력입니다.

- **무리함수 오차 모델 (거리 의존 오차)**  
  센서 거리 오차를 단순화한 모델:
  \[
  \sigma(r)=k\sqrt{r}
  \]
  여기서 $k$는 센서 특성 상수. 거리가 커질수록 오차가 증가하지만 증가율은 느려집니다.

- **신뢰도(score) 함수(예시)**  
  오차를 신뢰도로 바꾸는 한 예:
  \[
  T = \frac{1}{1+\sigma}
  \]
  → 오차가 작을수록 신뢰도 $T$는 1에 가깝고, 오차가 크면 0에 가까워집니다.

- **아폴로니우스의 원 (결정 경계의 기하)**  
  두 점 A, B에 대해 거리 비 $\dfrac{PA}{PB}=m$가 일정한 점들의 자취는 원(또는 특수한 직선)입니다.  
  → 신뢰도나 오차가 비율 형태로 결정될 때 경계선(두 센서가 동등한 지점)은 아폴로니우스 곡선으로 해석됩니다.

---

### 2) 그래프(등고선, contour) 읽는 법 — 핵심 포인트
1. **컬러바 먼저 보기**: 어떤 색이 큰 값(또는 작은 값)을 의미하는지 확인하세요.
2. **단일 센서 플롯**: 센서로부터의 거리/시간/오차 분포를 보여줍니다. 중심에서 멀어질수록 일반적으로 값이 증가(또는 변화)합니다.
3. **차이 맵(diff)**: $T_A - T_B$ 같은 차이 플롯에서 `0` 레벨(검은선)은 두 센서의 동등 지점 — 즉 결정 경계입니다.
4. **대칭성 검사**: 센서 배치가 대칭이라면 플롯도 대칭이어야 합니다. 비대칭이면 계산·좌표·센서 위치 입력을 확인하세요.
5. **급격한 색 변화(경계)**: 값이 빠르게 변하는 영역은 민감한 구간 — 작은 위치 변화로도 센서 선택이 바뀝니다.

---

### 3) 실전 해석 단계(권장 절차)
1. 관심 영역(예: 특정 x,y 블록) 선택.
2. 두 센서까지의 평균 거리·분산 계산 → 지역적 오차 수준 판단.
3. 신뢰도(T) 맵에서 임계값(예: 0.5) 근처 영역 확인 → 안정/불안정 구역 판별.
4. 차이 맵에서 0선(경계) 주변의 폭 확인 → 경계가 넓으면(완만) 전환이 부드럽고, 좁으면(급격) 불안정.
5. 파라미터 민감도: $k_A$, $k_B$ 값을 바꿔 결과(경계 위치·폭·평균 신뢰도) 변화 관찰.

---

### 4) 자주 묻는 질문(디버깅 중심)
- **왜 경계가 곡선인가요?**  
  거리 비(또는 신뢰도 비)가 위치에 따라 달라지므로 그 locus(자취)는 일반적으로 원·곡선입니다(아폴로니우스).
- **경계가 여러 개로 보이면?**  
  신호 모델이나 신뢰도 함수가 비선형(또는 이상치)일 가능성 — 데이터 스무딩 또는 모델 검토 필요.
- **색 지도가 이상하면?**  
  컬러맵 범위(최솟값·최댓값)가 자동 스케일링되어 일부 정보가 압축될 수 있음. 범위를 고정해 재검토하세요.

---

### 5) 해석을 위한 체크리스트 (순서대로)
- [ ] 센서 좌표가 올바른가? (Ax,Ay; Bx,By)
- [ ] 거리·오차 함수가 기대한 형태인가? ($\sigma=k\sqrt{r}$ 등)
- [ ] 컬러바 범위와 단위를 확인했는가? (m, cm, %, 등)
- [ ] 경계(0선)의 위치와 폭을 수치로 확인했는가? (교차 횟수, 경계 폭)
- [ ] 파라미터 변화(k 값 등)에 따른 민감도 실험을 했는가?

---

### 6) 한 줄 요약
> “거리 → 오차(무리함수) → 신뢰도(역함수 등) → 차이 맵 → 경계(아폴로니우스)”의 흐름으로 생각하면 모든 플롯이 직관적으로 연결됩니다.
    """)


# Footer
st.divider()
st.markdown("""
---
### 📚 학습 자료
- **무리함수**: σ(r) = k√r (거리에 따른 오차 증가)
- **아폴로니우스 원**: PA/PB = m/n (신뢰도 경계)
- **응용**: 자율주행차의 다중 센서 데이터 처리

**공통수학 2 단원**:
1. 도형의 방정식 (원, 극좌표)
2. 집합과 명제 (센서 선택 알고리즘)
3. 함수와 그래프 (무리함수, 신뢰도 함수)
""")
