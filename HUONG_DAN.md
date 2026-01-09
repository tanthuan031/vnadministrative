# Hướng Dẫn Sử Dụng File JSON

## 📁 Các File Đã Tạo

Bạn có **2 file JSON** để tra cứu thông tin hành chính:

1. **`old_to_new.json`** - Tra cứu từ CŨ sang MỚI
2. **`new_to_old.json`** - Tra cứu từ MỚI sang CŨ

---

## 📊 Thống Kê

### File `old_to_new.json`:
- **63** tỉnh/thành cũ
- **696** quận/huyện cũ  
- **10,038** xã/phường cũ

### File `new_to_old.json`:
- **34** tỉnh/thành mới
- **3,315** xã/phường mới

---

## 🔍 Cách Sử Dụng

### 1️⃣ File `old_to_new.json` - Tra cứu CŨ → MỚI

#### Cấu trúc:
```json
{
  "metadata": { ... },
  "provinces": {
    "<id_tỉnh_cũ>": {
      "old_province_id": "...",
      "old_province_name": "...",
      "new_province_id": "...",
      "new_province_name": "..."
    }
  },
  "districts": {
    "<id_quận_cũ>": {
      "old_district_id": "...",
      "old_district_name": "...",
      "old_province_id": "...",
      "old_province_name": "...",
      "new_province_id": "...",
      "new_province_name": "..."
    }
  },
  "wards": {
    "<id_xã_cũ>": {
      "old_ward_id": "...",
      "old_ward_name": "...",
      "old_district_id": "...",
      "old_district_name": "...",
      "old_province_id": "...",
      "old_province_name": "...",
      "new_ward_id": "...",
      "new_ward_name": "...",
      "new_province_id": "...",
      "new_province_name": "..."
    }
  }
}
```

#### Ví dụ sử dụng:

**Tra cứu xã cũ:**
```json
old_to_new.json → wards["65803"]
{
  "old_ward_id": "65803",
  "old_ward_name": "Phường Điện Biên",
  "old_district_id": "267",
  "old_district_name": "Quận Ba Đình",
  "old_province_id": "11",
  "old_province_name": "Thành Phố Hà Nội",
  "new_ward_id": "14091",
  "new_ward_name": "Phường Ba Đình",
  "new_province_id": "11",
  "new_province_name": "Thành Phố Hà Nội"
}
```

---

### 2️⃣ File `new_to_old.json` - Tra cứu MỚI → CŨ

#### Cấu trúc:
```json
{
  "metadata": { ... },
  "provinces": {
    "<id_tỉnh_mới>": {
      "new_province_id": "...",
      "new_province_name": "...",
      "old_provinces": [
        {
          "old_province_id": "...",
          "old_province_name": "..."
        }
      ],
      "total_old_provinces": 1
    }
  },
  "wards": {
    "<id_xã_mới>": {
      "new_ward_id": "...",
      "new_ward_name": "...",
      "new_province_id": "...",
      "new_province_name": "...",
      "old_wards": [
        {
          "old_ward_id": "...",
          "old_ward_name": "...",
          "old_district_id": "...",
          "old_district_name": "...",
          "old_province_id": "...",
          "old_province_name": "..."
        }
      ],
      "total_old_wards": 7
    }
  }
}
```

#### Ví dụ sử dụng:

**Tra cứu xã mới (có thể có nhiều xã cũ hợp nhất):**
```json
new_to_old.json → wards["14091"]
{
  "new_ward_id": "14091",
  "new_ward_name": "Phường Ba Đình",
  "new_province_id": "11",
  "new_province_name": "Thành Phố Hà Nội",
  "old_wards": [
    {
      "old_ward_id": "65803",
      "old_ward_name": "Phường Điện Biên",
      "old_district_id": "267",
      "old_district_name": "Quận Ba Đình",
      "old_province_id": "11",
      "old_province_name": "Thành Phố Hà Nội"
    },
    ... 6 xã cũ khác
  ],
  "total_old_wards": 7
}
```

---

## 💻 Code Mẫu Sử Dụng

### Python:
```python
import json

# Đọc file
with open('old_to_new.json', 'r', encoding='utf-8') as f:
    old_to_new = json.load(f)

with open('new_to_old.json', 'r', encoding='utf-8') as f:
    new_to_old = json.load(f)

# Tra cứu xã cũ -> xã mới
old_ward_id = "65803"
if old_ward_id in old_to_new['wards']:
    ward_info = old_to_new['wards'][old_ward_id]
    print(f"Xã cũ: {ward_info['old_ward_name']}")
    print(f"Xã mới: {ward_info['new_ward_name']}")

# Tra cứu xã mới -> xã cũ
new_ward_id = "14091"
if new_ward_id in new_to_old['wards']:
    ward_info = new_to_old['wards'][new_ward_id]
    print(f"Xã mới: {ward_info['new_ward_name']}")
    print(f"Có {ward_info['total_old_wards']} xã cũ:")
    for old_ward in ward_info['old_wards']:
        print(f"  - {old_ward['old_ward_name']}")
```

### JavaScript:
```javascript
// Đọc file
const oldToNew = require('./old_to_new.json');
const newToOld = require('./new_to_old.json');

// Tra cứu xã cũ -> xã mới
const oldWardId = "65803";
if (oldToNew.wards[oldWardId]) {
  const wardInfo = oldToNew.wards[oldWardId];
  console.log(`Xã cũ: ${wardInfo.old_ward_name}`);
  console.log(`Xã mới: ${wardInfo.new_ward_name}`);
}

// Tra cứu xã mới -> xã cũ
const newWardId = "14091";
if (newToOld.wards[newWardId]) {
  const wardInfo = newToOld.wards[newWardId];
  console.log(`Xã mới: ${wardInfo.new_ward_name}`);
  console.log(`Có ${wardInfo.total_old_wards} xã cũ:`);
  wardInfo.old_wards.forEach(oldWard => {
    console.log(`  - ${oldWard.old_ward_name}`);
  });
}
```

---

## 📌 Lưu Ý

1. **Tỉnh/Thành**: Một số tỉnh cũ có thể hợp nhất thành 1 tỉnh mới
2. **Quận/Huyện**: Trong cấu trúc mới, quận/huyện đã bị sáp nhập vào tỉnh/thành
3. **Xã/Phường**: Nhiều xã cũ có thể hợp nhất thành 1 xã mới
4. **ID**: Sử dụng ID để tra cứu chính xác, tránh nhầm lẫn do tên trùng

---

## 🔧 Script Tạo File

File được tạo bởi script: **`convert_to_two_files.py`**

Để chạy lại:
```bash
source venv/bin/activate
python convert_to_two_files.py
```
