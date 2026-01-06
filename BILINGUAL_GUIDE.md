# 雙語支援實施指南 / Bilingual Implementation Guide

## ✅ 完成項目 / What's Been Done

### 1. Django 國際化配置 / Django i18n Configuration
- ✅ 繁體中文 (Traditional Chinese) 為預設語言
- ✅ 英文作為第二語言
- ✅ LocaleMiddleware 中間件已添加
- ✅ 時區設定為台北 (Asia/Taipei)

### 2. 語言切換器 / Language Switcher
- ✅ 導航欄新增語言選擇器
- ✅ 🇹🇼 中文 / 🇬🇧 EN 標籤
- ✅ 自動提交表單切換語言
- ✅ 保留當前頁面位置

### 3. 翻譯文件 / Translation Files
- ✅ 建立 `locale/zh_Hant/LC_MESSAGES/django.po`
- ✅ 翻譯導航欄所有文本
- ✅ 編譯翻譯文件 (django.mo)

### 4. 已翻譯內容 / Translated Content
| 英文 (English) | 繁體中文 (Traditional Chinese) |
|----------------|-------------------------------|
| Buy | 購買 |
| Rent | 租賃 |
| Sell | 出售 |
| Agents | 經紀人 |
| About | 關於我們 |
| Hi | 您好 |
| Dashboard | 管理面板 |
| Logout | 登出 |
| Login | 登入 |
| Become an Agent | 成為經紀人 |
| Contact Us | 聯絡我們 |

---

## 🚀 如何測試 / How to Test

### 本地測試 / Local Testing
```bash
# 啟動開發伺服器
python manage.py runserver

# 開啟瀏覽器
http://localhost:8000/

# 點擊右上角語言選擇器
# Click language switcher in top-right corner
```

### 切換語言 / Switch Languages
1. **預設顯示**: 繁體中文 (Default: Traditional Chinese)
2. **選擇語言**: 點擊 "🇹🇼 中文" 或 "🇬🇧 EN"
3. **自動刷新**: 頁面會重新載入並顯示所選語言

---

## 📝 下一步：翻譯更多內容 / Next Steps: Translate More Content

### 優先翻譯頁面 / Priority Pages

#### 1. 首頁 (Homepage)
```django
{% load i18n %}
<h1>{% trans "Find Your Dream Home" %}</h1>
<p>{% trans "Browse thousands of properties" %}</p>
```

**需要翻譯 / To Translate**:
- "Find Your Dream Home" → "尋找您的夢想家園"
- "Browse thousands of properties" → "瀏覽數千個物業"
- "Featured Properties" → "精選物業"
- "View All Properties" → "查看所有物業"

#### 2. 物業列表 (Property List)
**需要翻譯 / To Translate**:
- "Homes for Sale" → "出售房屋"
- "Homes for Rent" → "出租房屋"
- "Filters" → "篩選"
- "Location" → "位置"
- "Price Range" → "價格範圍"
- "Property Type" → "物業類型"
- "Bedrooms" → "臥室"
- "Bathrooms" → "浴室"
- "Apply Filters" → "套用篩選"

#### 3. 物業詳情 (Property Detail)
**需要翻譯 / To Translate**:
- "Property Details" → "物業詳情"
- "Description" → "描述"
- "Features" → "特色"
- "Location" → "位置"
- "Contact Agent" → "聯絡經紀人"

#### 4. 登入/註冊 (Login/Register)
**需要翻譯 / To Translate**:
- "Email" → "電子郵件"
- "Password" → "密碼"
- "Remember Me" → "記住我"
- "Forgot Password?" → "忘記密碼？"
- "Sign Up" → "註冊"

---

## 🛠️ 如何新增翻譯 / How to Add Translations

### 步驟 1: 標記需要翻譯的文本 / Step 1: Mark Text for Translation

在模板中 / In templates:
```django
{% load i18n %}
<h1>{% trans "Your text here" %}</h1>
<p>{% blocktrans %}Longer text with {{ variable }}{% endblocktrans %}</p>
```

在 Python 代碼中 / In Python code:
```python
from django.utils.translation import gettext as _

message = _("This is translatable")
```

### 步驟 2: 生成翻譯文件 / Step 2: Generate Translation Files
```bash
python manage.py makemessages -l zh_Hant --ignore=.venv --ignore=staticfiles
```

### 步驟 3: 編輯翻譯 / Step 3: Edit Translations
打開文件 / Open file:
```
locale/zh_Hant/LC_MESSAGES/django.po
```

添加翻譯 / Add translations:
```po
msgid "Find Your Dream Home"
msgstr "尋找您的夢想家園"
```

### 步驟 4: 編譯翻譯 / Step 4: Compile Translations
```bash
python manage.py compilemessages
```

### 步驟 5: 測試 / Step 5: Test
```bash
python manage.py runserver
```

---

## 🇹🇼 台灣本地化建議 / Taiwan Localization Recommendations

### 1. 幣別 (Currency)
```python
# 顯示台幣和美金
價格: NT$5,000,000 (約 US$166,000)
```

### 2. 面積單位 (Area Units)
```python
# 台灣常用「坪」
面積: 30坪 (約 99平方米 / 1,066平方英尺)
# 1坪 = 3.3058平方米 = 35.58平方英尺
```

### 3. 地址格式 (Address Format)
```
台灣格式: 花蓮縣花蓮市中正路123號
Western format: No. 123, Zhongzheng Rd., Hualien City, Hualien County
```

### 4. 電話格式 (Phone Format)
```
台灣格式: (03) 8123-4567
國際格式: +886 3 8123-4567
行動電話: 0912-345-678
```

### 5. 物業類型 (Property Types)
| 英文 | 繁體中文 | 說明 |
|------|----------|------|
| House | 透天厝 | Stand-alone house |
| Apartment | 公寓 | Apartment (usually no elevator) |
| Condo | 電梯大樓 | Condo/High-rise |
| Villa | 別墅 | Villa |
| Land | 土地 | Land |

### 6. 台灣特色功能 (Taiwan-Specific Features)

#### 風水資訊 (Feng Shui)
```python
# 模型字段
feng_shui_notes = models.TextField(blank=True, verbose_name="風水說明")
```

#### 學區 (School District)
```python
school_district = models.CharField(max_length=100, blank=True, verbose_name="學區")
```

#### 捷運站距離 (MRT Distance) - 適用台北
```python
nearest_mrt = models.CharField(max_length=100, blank=True, verbose_name="最近捷運站")
mrt_distance_mins = models.IntegerField(null=True, blank=True, verbose_name="步行分鐘")
```

---

## 💰 台灣市場定價策略 / Taiwan Market Pricing

### 目標客戶 (Target Clients)
1. **小型仲介公司 (Small Agencies)** - 1-5位經紀人
   - 價格: NT$15,000-30,000/年
   - 特點: 基本功能 + 無限物件

2. **中型仲介公司 (Medium Agencies)** - 6-20位經紀人
   - 價格: NT$50,000-100,000/年
   - 特點: 進階功能 + 多用戶管理

3. **安裝費用 (Setup Fee)**
   - 價格: NT$10,000-20,000
   - 包含: 資料匯入 + 訓練 + 客製化

### 價值主張 (Value Proposition)
```
✅ 專業房仲管理系統 (Professional real estate management)
✅ 雙語國際標準 (Bilingual international standard)
✅ 無限物件刊登 (Unlimited property listings)
✅ 行動裝置友善 (Mobile-friendly)
✅ 專業客戶管理 (Professional CRM)
✅ 花蓮在地支援 (Local Hualien support)
```

---

## 📱 花蓮市場策略 / Hualien Market Strategy

### 競爭優勢 (Competitive Advantages)
1. **現代化系統** - 比 Excel 和 Facebook 專業
2. **雙語支援** - 適合國際買家
3. **行動友善** - 隨時隨地管理
4. **在地價格** - 比台北系統便宜
5. **本地支援** - 花蓮在地服務

### 目標客戶 (Target Clients)
- 永慶房屋花蓮分店
- 信義房屋花蓮店
- 住商不動產花蓮
- 東森房屋花蓮
- 在地小型仲介

### 銷售話術 (Sales Pitch)
```
"專業如台北大公司，價格如花蓮在地"
"Professional like Taipei companies, priced for Hualien"

特點:
✓ 雙語系統 - 服務國際客戶
✓ 行動裝置 - 隨時更新物件
✓ 專業形象 - 提升公司品牌
✓ 簡單易用 - 10分鐘學會
✓ 在地支援 - 花蓮現場服務
```

---

## 🚀 部署到 Railway (Deployment)

### 雙語設定保持不變 / Bilingual Settings Remain Same
部署到 Railway 時，系統自動:
1. **預設語言**: 繁體中文
2. **自動偵測**: 根據瀏覽器語言
3. **手動切換**: 右上角語言選擇器

### 環境變數不變 / Environment Variables Unchanged
```env
SECRET_KEY=<your-key>
DEBUG=False
ALLOWED_HOSTS=your-app.up.railway.app
DATABASE_URL=<auto-provided>
```

---

## ✅ 完成清單 / Checklist

### 已完成 (Completed)
- [x] Django i18n 配置
- [x] 語言切換器
- [x] 導航欄翻譯
- [x] 時區設定 (Asia/Taipei)
- [x] 翻譯文件結構

### 待完成 (To Do)
- [ ] 首頁翻譯
- [ ] 物業列表頁翻譯
- [ ] 物業詳情頁翻譯
- [ ] 登入/註冊表單翻譯
- [ ] 經紀人儀表板翻譯
- [ ] 錯誤訊息翻譯
- [ ] 電子郵件模板翻譯

### 台灣特色功能 (Taiwan-Specific)
- [ ] 坪數計算器
- [ ] 風水資訊欄位
- [ ] 學區資訊
- [ ] 台幣顯示
- [ ] 台灣地址格式

---

## 📚 資源 (Resources)

### Django i18n 文檔
- https://docs.djangoproject.com/en/6.0/topics/i18n/

### 翻譯工具 (Translation Tools)
- **Google Translate**: https://translate.google.com/
- **DeepL**: https://www.deepl.com/ (更準確的中文翻譯)
- **104人力銀行**: 找專業譯者 (NT$500-1000)

### 台灣房地產術語
- 內政部不動產交易實價查詢: https://lvr.land.moi.gov.tw/
- 台灣房屋專業術語參考

---

## 🎯 30天行動計劃 / 30-Day Action Plan

### 第1週 (Week 1): 完成核心翻譯
- 翻譯首頁、物業列表、物業詳情
- 測試語言切換功能
- 修正任何顯示問題

### 第2週 (Week 2): 台灣本地化
- 添加坪數計算
- 添加台幣顯示
- 設計台灣地址格式

### 第3週 (Week 3): 市場準備
- 準備示範網站
- 製作銷售簡報
- 聯絡花蓮仲介公司

### 第4週 (Week 4): 首次銷售
- 約見2-3家仲介
- 現場展示系統
- 收集反饋意見

---

## 💡 下一步行動 / Next Actions

1. **繼續翻譯**: 執行上述翻譯步驟
2. **本地測試**: 確保切換語言正常
3. **部署測試**: 推送到 Railway 測試
4. **市場推廣**: 準備銷售資料

**需要協助嗎？/ Need Help?**
我可以幫助:
- 翻譯更多頁面
- 添加台灣特色功能
- 優化本地化設定

---

**建立日期 / Created**: 2026年1月6日  
**版本 / Version**: 1.0  
**狀態 / Status**: ✅ 基礎雙語支援已完成 / Basic Bilingual Support Complete
