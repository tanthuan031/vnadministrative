# Vietnam Administrative Data API

> Dữ liệu hành chính Việt Nam (Tỉnh/Thành, Quận/Huyện, Xã/Phường) - Mapping giữa cấu trúc cũ và mới

## 📊 Thống Kê

- **63** tỉnh/thành cũ → **34** tỉnh/thành mới
- **696** quận/huyện cũ (đã sáp nhập vào tỉnh/thành mới)
- **10,038** xã/phường cũ → **3,315** xã/phường mới

## 🔗 API Endpoints (Raw JSON)

### Option 1: Complete Data Files

#### Cấu trúc CŨ (Old Structure)

```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/old_to_new.json
```

**Bao gồm:**
- `provinces` - Tỉnh/Thành cũ → mới
- `districts` - Quận/Huyện cũ → mới
- `wards` - Xã/Phường cũ → mới

#### Cấu trúc MỚI (New Structure)

```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/new_to_old.json
```

**Bao gồm:**
- `provinces` - Tỉnh/Thành mới → danh sách tỉnh cũ
- `wards` - Xã/Phường mới → danh sách xã cũ

### Option 2: API-Style (Recommended for Dropdowns)

#### 1. Get All Provinces
```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/provinces.json
```
Returns: Array of 63 provinces

#### 2. Get Districts by Province
```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/districts/{province_id}.json
```
Example: `api/districts/11.json` (Hà Nội)

#### 3. Get Wards by District
```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/wards/{district_id}.json
```
Example: `api/wards/267.json` (Ba Đình)

## 💻 Cách Sử Dụng

### API-Style for Cascading Dropdowns (Recommended)

```javascript
const BASE_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api';

// 1. Load provinces
async function loadProvinces() {
  const response = await fetch(`${BASE_URL}/provinces.json`);
  return await response.json();
}

// 2. Load districts by province
async function loadDistricts(provinceId) {
  const response = await fetch(`${BASE_URL}/districts/${provinceId}.json`);
  return await response.json();
}

// 3. Load wards by district
async function loadWards(districtId) {
  const response = await fetch(`${BASE_URL}/wards/${districtId}.json`);
  return await response.json();
}

// Usage
const provinces = await loadProvinces();
const districts = await loadDistricts('11'); // Hà Nội
const wards = await loadWards('267'); // Ba Đình
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
