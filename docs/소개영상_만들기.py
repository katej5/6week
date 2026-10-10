"""README용 소개 영상(약 50초, 1280x720, 무음)을 만든다."""
import sys
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
W, H, FPS = 1280, 720, 30
F = "C:/Windows/Fonts/"
def font(size, bold=False):
    return ImageFont.truetype(F + ("malgunbd.ttf" if bold else "malgun.ttf"), size)

BG = (18, 22, 30); FG = (236, 239, 244); SUB = (150, 160, 178)
ACC = (94, 167, 255); WARN = (255, 184, 77); STOP = (255, 107, 107); OK = (110, 214, 150)
PANEL = (32, 39, 52)

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

# 장면 = (길이초, 그리기함수(draw, img, t초))
def txt(d, xy, s, f, c, a=1.0, anchor="la"):
    c = tuple(int(BG[i] + (c[i] - BG[i]) * a) for i in range(3))
    d.text(xy, s, font=f, fill=c, anchor=anchor)

def header(d, t, title, kicker):
    a = ease(t / 0.5)
    txt(d, (80, 60), kicker, font(22, True), ACC, a)
    txt(d, (80, 95), title, font(44, True), FG, a)

def s_title(d, img, t):
    a = ease(t / 0.8)
    txt(d, (W//2, 250), "6week", font(30, True), ACC, a, "mm")
    txt(d, (W//2, 320), "글쓰기 파이프라인", font(68, True), FG, a, "mm")
    b = ease((t - 1.0) / 0.8)
    txt(d, (W//2, 420), "주제 카드 하나  →  게시 직전 원고 한 폴더", font(32), SUB, b, "mm")
    c = ease((t - 2.2) / 0.8)
    txt(d, (W//2, 600), "신흥기술세미나 실습 · Claude Code 스킬", font(22), SUB, c, "mm")

def s_problem(d, img, t):
    header(d, t, "글 한 편에 하루 이상 걸렸습니다", "왜 만들었나")
    items = ["관심 있는 주제인지 가늠하기", "원문을 직접 열어 인용·수치 대조",
             "내 말투로 고쳐 쓰기", "이미지 만들기", "편집 기준으로 검수"]
    for i, s in enumerate(items):
        a = ease((t - 0.8 - i * 0.45) / 0.5)
        y = 200 + i * 70
        d.rounded_rectangle((80, y, 760, y + 54), 10, fill=tuple(int(BG[k]+(PANEL[k]-BG[k])*a) for k in range(3)))
        txt(d, (105, y + 27), f"{i+1}.  {s}", font(28), FG, a, "lm")
    a = ease((t - 3.6) / 0.6)
    txt(d, (830, 330), "모두 손으로", font(40, True), WARN, a)
    txt(d, (830, 390), "→ 단계를 쪼개고", font(28), FG, a)
    txt(d, (830, 430), "→ 결과를 파일로 남기고", font(28), FG, a)
    txt(d, (830, 470), "→ 사람 자리에서 멈춘다", font(28), FG, a)

STEPS = [("1", "기획", "01_기획.md"), ("2", "관심도", "02_관심도.md"), ("3", "원문 조사", "03_원문.md"),
         ("4", "출처 신뢰", "04_출처.md"), ("5", "집필", "05_초고.md"), ("6", "이미지", "06_이미지/"),
         ("7", "검수", "07_검수.md"), ("8", "저장", "08_최종.md")]
def s_steps(d, img, t):
    header(d, t, "8단계, 단계마다 파일 하나", "어떻게 움직이나")
    bw, bh, gx = 270, 150, 26
    for i, (n, name, f) in enumerate(STEPS):
        a = ease((t - 0.6 - i * 0.4) / 0.4)
        col, row = i % 4, i // 4
        x = 80 + col * (bw + gx); y = 200 + row * (bh + 40)
        fill = tuple(int(BG[k]+(PANEL[k]-BG[k])*a) for k in range(3))
        d.rounded_rectangle((x, y, x + bw, y + bh), 14, fill=fill)
        txt(d, (x + 22, y + 20), n, font(34, True), ACC, a)
        txt(d, (x + 22, y + 66), name, font(32, True), FG, a)
        txt(d, (x + 22, y + 112), f, font(20), SUB, a)
        if col < 3:
            txt(d, (x + bw + gx // 2, y + bh // 2), "›", font(30, True), SUB, a, "mm")
    a = ease((t - 4.4) / 0.6)
    txt(d, (W//2, 640), "검수(7)는 만든 과정을 모르는 서브에이전트가 맡습니다", font(24), SUB, a, "mm")

def s_stop(d, img, t):
    header(d, t, "핵심은 빨리 끝내는 게 아니라 '멈추는 것'", "멈춤 규칙")
    rows = [("[자료 부족]", "원문을 못 열었거나 출처가 기준 미달 · 문체 샘플 2편 미만", WARN),
            ("[사람 판단]", "관심도 '낮음' · 검수 2회차에도 [필수] 지적이 남음", STOP),
            ("[게시 승인]", "8단계 끝 — 게시는 언제나 사람이 직접", OK)]
    for i, (k, v, c) in enumerate(rows):
        a = ease((t - 0.8 - i * 0.8) / 0.5)
        y = 210 + i * 110
        d.rounded_rectangle((80, y, 1200, y + 86), 12, fill=tuple(int(BG[j]+(PANEL[j]-BG[j])*a) for j in range(3)))
        d.rectangle((80, y, 88, y + 86), fill=tuple(int(BG[j]+(c[j]-BG[j])*a) for j in range(3)))
        txt(d, (115, y + 43), k, font(30, True), c, a, "lm")
        txt(d, (340, y + 43), v, font(26), FG, a, "lm")
    a = ease((t - 3.6) / 0.6)
    txt(d, (80, 580), "멈출 때마다 진행상태.md에  어디서 · 왜 · 무엇을 해 주면 이어 가는지  기록", font(26), FG, a)
    txt(d, (80, 625), "→ 중간에 끊겨도 그 파일 하나로 이어 갑니다", font(26), ACC, a)

def s_source(d, img, t):
    header(d, t, "모든 사실 주장엔 근거가 붙어야 통과", "근거 기준")
    grades = [("A", "1차 원문", "법령·고시 · 공공기관 자료 · 공식 문서 · 논문", OK),
              ("B", "2차 해설", "원문을 밝힌 언론·전문매체 · 연구기관·로펌 해설", ACC),
              ("C", "실마리만", "블로그 · 커뮤니티 · 위키 · AI 요약 → 근거로 안 씀", STOP)]
    for i, (g, n, v, c) in enumerate(grades):
        a = ease((t - 0.7 - i * 0.6) / 0.5)
        y = 200 + i * 95
        d.ellipse((80, y, 150, y + 70), fill=tuple(int(BG[j]+(c[j]-BG[j])*a) for j in range(3)))
        txt(d, (115, y + 35), g, font(34, True), BG if a > .5 else FG, a, "mm")
        txt(d, (175, y + 12), n, font(28, True), FG, a)
        txt(d, (360, y + 16), v, font(24), SUB, a)
    a = ease((t - 2.8) / 0.6)
    d.rounded_rectangle((80, 500, 1200, 640), 14, fill=tuple(int(BG[j]+(PANEL[j]-BG[j])*a) for j in range(3)))
    txt(d, (W//2, 545), "A 1개   또는   서로 독립된 B 2개", font(36, True), FG, a, "mm")
    txt(d, (W//2, 600), "출처마다 주소 · 열람일 · 확인 위치 — 없으면 〔확인 필요〕로 남김", font(24), SUB, a, "mm")

def s_use(d, img, t):
    header(d, t, "써 보려면", "Claude Code에서")
    lines = [("# 새로 시작", SUB), ("/writing-pipeline raw/주제카드_내주제.md", OK), ("", FG),
             ("# 멈춘 지점부터 이어 가기", SUB), ("/writing-pipeline out/2026-10-06_생성형AI-표시의무", OK)]
    a0 = ease((t - 0.5) / 0.5)
    d.rounded_rectangle((80, 190, 1200, 440), 14, fill=tuple(int(BG[j]+((10,13,18)[j]-BG[j])*a0) for j in range(3)))
    for i, (s, c) in enumerate(lines):
        a = ease((t - 0.9 - i * 0.35) / 0.4)
        txt(d, (115, 220 + i * 42), s, font(26) if s.startswith("/") else font(24), c, a)
    a = ease((t - 2.8) / 0.6)
    txt(d, (80, 490), "raw/ 에 넣을 것", font(26, True), ACC, a)
    txt(d, (80, 535), "주제 카드  ·  내가 공개한 글 2편 이상(문체 샘플)  ·  편집 기준", font(26), FG, a)

def s_end(d, img, t):
    a = ease(t / 0.8)
    txt(d, (W//2, 280), "AI가 쓰고, 사람이 정합니다", font(54, True), FG, a, "mm")
    b = ease((t - 1.0) / 0.8)
    txt(d, (W//2, 370), "근거 없는 문장은 쓰지 않고, 사람이 정할 자리에서는 멈춥니다", font(28), SUB, b, "mm")
    c = ease((t - 2.0) / 0.8)
    txt(d, (W//2, 480), "github.com/katej5/6week", font(28, True), ACC, c, "mm")

SCENES = [(5, s_title), (7, s_problem), (8, s_steps), (7.5, s_stop), (7.5, s_source), (6.5, s_use), (5, s_end)]

w = imageio.get_writer(OUT, fps=FPS, codec="libx264", quality=8, pixelformat="yuv420p", macro_block_size=8)
total = sum(s for s, _ in SCENES); done = 0
for i, (dur, fn) in enumerate(SCENES):
    n = int(dur * FPS)
    for k in range(n):
        t = k / FPS
        img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
        fn(d, img, t)
        # 진행 막대
        p = (done + t) / total
        d.rectangle((0, H - 6, int(W * p), H), fill=ACC)
        # 장면 끝 0.4초 페이드아웃
        fo = (dur - t) / 0.4
        arr = np.asarray(img).astype(np.float32)
        if fo < 1 and i < len(SCENES) - 1:
            arr = np.array(BG, np.float32) + (arr - np.array(BG, np.float32)) * max(fo, 0)
        w.append_data(arr.astype(np.uint8))
        if i == 0 and k == 0: poster = None
    done += dur
w.close()
print("ok", total, "s")
