import json
import datetime
import calendar
import requests
import os
from svgwrite import Drawing
from svgwrite.animate import Animate

# Constants from github_heatmap.config
COLOR_TUPLE = [
    ("#4DD2FF", "#FF6B6B", "#FFE66D"),
    ("#4DD2FF", "#FF6B6B", "#FFE66D"),
    ("#4DD2FF", "#FF6B6B", "#FFE66D"),
]
DEFAULT_DOM_COLOR = "#f7f7f7"  # 修改空白格子背景色
DOM_BOX_DICT = {
    1: {"dom": [(10, 10)]},
    2: {"dom": [(10, 5), (10, 5)]},
    3: {"dom": [(10, 3), (10, 3), (10, 4)]},
}
DOM_BOX_TUPLE = (10, 10)
MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
YEAR_FONT_SIZE = 14
MONTH_FONT_SIZE = 10
DOM_BOX_PADING = 2
DOM_BOX_RADIUS = 2
WEREAD_COOKIE = "wr_fp=1762718669; wr_vid=365204818; wr_rt=web%40YjBCvyrOXJguITRcOMh_AL; wr_skey=1jgkQQzq"

class Drawer:
    name = "readtime"

    def __init__(self, p):
        self.poster = p
        self.year_style = f"font-size:{YEAR_FONT_SIZE}px; font-family:Arial;"
        self.month_names_style = f"font-size:{MONTH_FONT_SIZE}px; font-family:Arial"

    def _process_read_times(self, read_times):
        tracks = {}
        for timestamp, duration in read_times.items():
            date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
            tracks[date] = duration
        return tracks

    def make_color(self, length_range, length):
        color_from = self.poster.colors["track"]
        color_to = self.poster.colors["special2"]
        diff = length_range.diameter()
        if diff == 0:
            return color_from

        return self.interpolate_color(
            color_from, color_to, (length - length_range.lower) / diff
        )

    def interpolate_color(self, color_from, color_to, ratio):
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        from_rgb = hex_to_rgb(color_from)
        to_rgb = hex_to_rgb(color_to)
        result = tuple(int(from_rgb[i] + (to_rgb[i] - from_rgb[i]) * ratio) for i in range(3))
        return rgb_to_hex(result)

    def _gen_day_box(self, dr, rect_x, rect_y, date_title, day_tracks):
        color = DEFAULT_DOM_COLOR  # 使用 DEFAULT_DOM_COLOR
        if day_tracks:
            color = self.make_color(self.poster.length_range_by_date, day_tracks)
            date_title = f"{date_title} {day_tracks} {self.poster.units}"
        rect = dr.rect(
            (rect_x, rect_y),
            DOM_BOX_TUPLE,
            fill=color,
            rx=DOM_BOX_RADIUS,
            ry=DOM_BOX_RADIUS,
        )
        rect.set_desc(title=date_title)
        return rect

    def _draw_one_calendar(self, dr, year, offset):
        start_date_weekday, _ = calendar.monthrange(year, 1)
        github_rect_first_day = datetime.date(year, 1, 1)
        github_rect_day = github_rect_first_day + datetime.timedelta(-start_date_weekday)

        year_length = self.poster.total_sum_year_dict.get(year, 0)
        year_units = "hours"  # 修改单位为小时
        year_length = str(int(year_length / 3600)) + f" {year_units}"  # 秒转换为小时

        offset.y += DOM_BOX_PADING + YEAR_FONT_SIZE
        dr.add(
            dr.text(
                f"{year}: {year_length}",
                insert=offset.tuple(),
                fill=self.poster.colors["text"],
                style=self.year_style,
            )
        )
        offset.y += DOM_BOX_PADING + MONTH_FONT_SIZE

        size = DOM_BOX_PADING + DOM_BOX_TUPLE[1]
        rect_x = offset.x
        month = MONTH_NAMES[0]

        for index in range(54):
            if index == 0:
                dr.add(
                    dr.text(
                        f"{month}",
                        insert=(rect_x, offset.y),
                        fill=self.poster.colors["text"],
                        style=self.month_names_style,
                    )
                )
            if index > 0 and index < 53 and month != MONTH_NAMES[github_rect_day.month - 1]:
                month = MONTH_NAMES[github_rect_day.month - 1]
                dr.add(
                    dr.text(
                        f"{month}",
                        insert=(rect_x, offset.y),
                        fill=self.poster.colors["text"],
                        style=self.month_names_style,
                    )
                )

            for week in range(7):
                if int(github_rect_day.year) > year:
                    break
                rect_y = offset.y + size * week + DOM_BOX_PADING
                date_title = str(github_rect_day)
                day_tracks = self.poster.tracks.get(date_title)
                rect = self._gen_day_box(dr, rect_x, rect_y, date_title, day_tracks)
                dr.add(rect)
                github_rect_day += datetime.timedelta(1)
            rect_x += size
        offset.y += size * 7

    def draw(self, dr, offset, is_summary=False):
        if self.poster.tracks is None:
            raise Exception("No tracks to draw")

        # 增加显示的年份区间配置
        start_year = self.poster.start_year if hasattr(self.poster, 'start_year') else self.poster.years[0]
        end_year = self.poster.end_year if hasattr(self.poster, 'end_year') else self.poster.years[-1]
        for year in range(start_year, end_year + 1)[::-1]:
            self._draw_one_calendar(dr, year, offset)

def get_readtiming_data(cookie):
    url = "https://i.weread.qq.com/readdata/summary?synckey=0"
    headers = {
        "Cookie": cookie
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return {"errCode": 1001, "message": "未授权，请重新登录"}
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def refresh_cookies(cookie):
        """
        尝试通过API刷新cookies
        
        注意: 微信读书没有公开的API用于刷新令牌。
        这是一个模拟实现 - 实际操作中，您可能需要:
        1. 使用无头浏览器如Selenium或Playwright
        2. 实现二维码扫描流程
        3. 或定期手动更新cookies
        
        返回:
            元组 (是否成功, 新的cookies)
        """
        print("尝试刷新cookies...")
        print("注意: 由于微信读书的认证系统通常需要扫描二维码，")
        print("因此可能无法在没有用户交互的情况下实现完全自动刷新。")
        
        url = "https://weread.qq.com/"
        headers = {
            "Cookie": cookie
        }
        
        try:
            response = requests.get(url, headers=headers)
            new_cookies = response.cookies.get_dict()
            
            # 更新cookie
            cookie_parts = cookie.split(';')
            updated_cookie = []
            for part in cookie_parts:
                key = part.split('=')[0].strip()
                if key not in new_cookies:
                    updated_cookie.append(part)
            
            for key, value in new_cookies.items():
                updated_cookie.append(f"{key}={value}")
            
            updated_cookie_str = '; '.join(updated_cookie)
            print("已生成新的cookie")
            return True, updated_cookie_str
        except Exception as e:
            print(f"刷新cookies时出错: {e}")
            return False, None

def main():
    cookie = os.getenv("WEREAD_COOKIE")  # 从环境变量中获取 cookie?
    if not cookie:
        raise Exception("WEREAD_COOKIE environment variable is required")
    
    data = None  # 初始化data变量

    try:
        data = get_readtiming_data(cookie)
        if data.get("errCode") == 1001:  # 假设1001表示未登录
            print("检测到未登录状态，尝试刷新cookies...")
            success, new_cookie = refresh_cookies(cookie)
            if success:
                print("cookies刷新成功，重新获取数据...")
                cookie = new_cookie
                data = get_readtiming_data(cookie)
                if data.get("errCode") == 1001:
                    print("自动刷新cookies后仍然未登录")
            else:
                print("cookies刷新失败，请手动更新cookies")
    except Exception as e:
        print(f"获取阅读数据时出错: {e}")

    class Poster:
        def __init__(self):
            self.tracks = None
            self.years = []
            self.colors = {
                "track": "#4DD2FF",
                "special": "#FF6B6B",
                "special2": "#FFE66D",
                "text": "#2D3436",
                "dom": "#f7f7f7"  # 修改空白格子背景色
            }
            self.units = "secs"
            self.with_animation = False
            self.type_list = ["readtime"]
            self.special_number = {
                "special_number1": 3600,
                "special_number2": 1800
            }
            self.length_range_by_date = None
            self.total_sum_year_dict = {}
            self.start_year = int(os.getenv("START_YEAR", 2020))  # 从环境变量中获取开始年份
            self.end_year = int(os.getenv("END_YEAR", 2025))  # 从环境变量中获取结束年份

    poster = Poster()
    drawer = Drawer(poster)

    if data is None:
        print("无法获取阅读数据，请检查网络连接或cookie是否有效")
        return
        
    tracks = drawer._process_read_times(data['readTimes'])
    poster.tracks = tracks

    dates = list(tracks.keys())
    years = sorted(list(set([int(date.split('-')[0]) for date in dates])))
    poster.years = [min(years), max(years)]  # 配置显示的年份区间

    durations = list(tracks.values())
    poster.length_range_by_date = Range(min(durations), max(durations))

    for year in years:
        total = sum([duration for date, duration in tracks.items() if date.startswith(str(year))])
        poster.total_sum_year_dict[year] = total
    
    # 动态计算 SVG 高度
    year_count = poster.end_year - poster.start_year + 1
    svg_height = 100 + year_count * 115  # 每增加一年，高度增加 200

    dr = Drawing('heatmap.svg', size=(800, svg_height))
    offset = Offset(50, 50)
    drawer.draw(dr, offset)
    dr.save()

class Range:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def diameter(self):
        return self.upper - self.lower

class Offset:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)

if __name__ == '__main__':
    main()
