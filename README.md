# Vietnam Administrative Data API

> Dữ liệu hành chính Việt Nam (Tỉnh/Thành, Quận/Huyện, Xã/Phường) - Mapping giữa cấu trúc cũ và mới

## 📊 Thống Kê

- **63** tỉnh/thành cũ → **34** tỉnh/thành mới
- **696** quận/huyện cũ (đã sáp nhập vào tỉnh/thành mới)
- **10,038** xã/phường cũ → **3,315** xã/phường mới

## 🔗 API Endpoints (Raw JSON)

### Cấu trúc CŨ (Old Structure)

```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/old_to_new.json
```

**Bao gồm:**
- `provinces` - Tỉnh/Thành cũ → mới
- `districts` - Quận/Huyện cũ → mới
- `wards` - Xã/Phường cũ → mới

### Cấu trúc MỚI (New Structure)

```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/new_to_old.json
```

**Bao gồm:**
- `provinces` - Tỉnh/Thành mới → danh sách tỉnh cũ
- `wards` - Xã/Phường mới → danh sách xã cũ

## 💻 Cách Sử Dụng

### JavaScript/TypeScript

```javascript
// Fetch dữ liệu từ GitHub
const OLD_TO_NEW_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/old_to_new.json';
const NEW_TO_OLD_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/new_to_old.json';

// Lấy dữ liệu cũ → mới
async function getOldToNew() {
  const response = await fetch(OLD_TO_NEW_URL);
  return await response.json();
}

// Lấy dữ liệu mới → cũ
async function getNewToOld() {
  const response = await fetch(NEW_TO_OLD_URL);
  return await response.json();
}

// Ví dụ: Tra cứu xã cũ
const data = await getOldToNew();
const ward = data.wards['65803'];
console.log(`${ward.old_ward_name} → ${ward.new_ward_name}`);
```

### Python

```python
import requests

OLD_TO_NEW_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/old_to_new.json'
NEW_TO_OLD_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/new_to_old.json'

# Lấy dữ liệu cũ → mới
response = requests.get(OLD_TO_NEW_URL)
old_to_new = response.json()

# Tra cứu xã cũ
ward = old_to_new['wards']['65803']
print(f"{ward['old_ward_name']} → {ward['new_ward_name']}")
```

### React/Next.js

```typescript
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

function useAdminData() {
  const { data: oldToNew } = useSWR(
    'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/old_to_new.json',
    fetcher
  );
  
  const { data: newToOld } = useSWR(
    'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/new_to_old.json',
    fetcher
  );
  
  return { oldToNew, newToOld };
}
```

## 📖 Cấu Trúc Dữ Liệu

### old_to_new.json

```json
{
  "metadata": {
    "title": "Mapping Hành Chính: Cũ → Mới",
    "total_records": 10358
  },
  "provinces": {
    "<id_tỉnh_cũ>": {
      "old_province_id": "11",
      "old_province_name": "Thành Phố Hà Nội",
      "new_province_id": "11",
      "new_province_name": "Thành Phố Hà Nội"
    }
  },
  "districts": {
    "<id_quận_cũ>": {
      "old_district_id": "267",
      "old_district_name": "Quận Ba Đình",
      "old_province_id": "11",
      "old_province_name": "Thành Phố Hà Nội",
      "new_province_id": "11",
      "new_province_name": "Thành Phố Hà Nội"
    }
  },
  "wards": {
    "<id_xã_cũ>": {
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
  }
}
```

### new_to_old.json

```json
{
  "metadata": {
    "title": "Mapping Hành Chính: Mới → Cũ",
    "total_records": 10358
  },
  "provinces": {
    "<id_tỉnh_mới>": {
      "new_province_id": "11",
      "new_province_name": "Thành Phố Hà Nội",
      "old_provinces": [
        {
          "old_province_id": "11",
          "old_province_name": "Thành Phố Hà Nội"
        }
      ],
      "total_old_provinces": 1
    }
  },
  "wards": {
    "<id_xã_mới>": {
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
        }
      ],
      "total_old_wards": 7
    }
  }
}
```
