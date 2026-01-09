# Hướng Dẫn Sử Dụng API

## 🌐 API Endpoints

### 1. Lấy Danh Sách Tỉnh/Thành
```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/provinces.json
```
Trả về: Array gồm 63 tỉnh/thành

### 2. Lấy Danh Sách Quận/Huyện Theo Tỉnh
```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/districts/{province_id}.json
```
**Ví dụ:** `api/districts/11.json` (Hà Nội)

### 3. Lấy Danh Sách Xã/Phường Theo Quận
```
https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/wards/{district_id}.json
```
**Ví dụ:** `api/wards/267.json` (Ba Đình)

---

## 💻 Code Mẫu

### JavaScript/TypeScript

```javascript
const BASE_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api';

// 1. Load tỉnh/thành
async function loadProvinces() {
  const response = await fetch(`${BASE_URL}/provinces.json`);
  const provinces = await response.json();
  return provinces; // [{id: "11", name: "Thành Phố Hà Nội", ...}, ...]
}

// 2. Load quận/huyện theo tỉnh
async function loadDistricts(provinceId) {
  const response = await fetch(`${BASE_URL}/districts/${provinceId}.json`);
  const districts = await response.json();
  return districts; // [{id: "267", name: "Quận Ba Đình", ...}, ...]
}

// 3. Load xã/phường theo quận
async function loadWards(districtId) {
  const response = await fetch(`${BASE_URL}/wards/${districtId}.json`);
  const wards = await response.json();
  return wards; // [{id: "65803", name: "Phường Điện Biên", ...}, ...]
}

// Sử dụng
const provinces = await loadProvinces();
const districts = await loadDistricts('11'); // Hà Nội
const wards = await loadWards('267'); // Ba Đình
```

### React Example

```jsx
import { useState, useEffect } from 'react';

function AddressSelector() {
  const [provinces, setProvinces] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [wards, setWards] = useState([]);
  
  const [selectedProvince, setSelectedProvince] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [selectedWard, setSelectedWard] = useState('');

  const BASE_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api';

  // Load tỉnh khi component mount
  useEffect(() => {
    fetch(`${BASE_URL}/provinces.json`)
      .then(res => res.json())
      .then(data => setProvinces(data));
  }, []);

  // Load quận khi chọn tỉnh
  useEffect(() => {
    if (selectedProvince) {
      fetch(`${BASE_URL}/districts/${selectedProvince}.json`)
        .then(res => res.json())
        .then(data => setDistricts(data));
      setSelectedDistrict('');
      setWards([]);
    }
  }, [selectedProvince]);

  // Load xã khi chọn quận
  useEffect(() => {
    if (selectedDistrict) {
      fetch(`${BASE_URL}/wards/${selectedDistrict}.json`)
        .then(res => res.json())
        .then(data => setWards(data));
      setSelectedWard('');
    }
  }, [selectedDistrict]);

  return (
    <div>
      <select value={selectedProvince} onChange={(e) => setSelectedProvince(e.target.value)}>
        <option value="">Chọn Tỉnh/Thành</option>
        {provinces.map(p => (
          <option key={p.id} value={p.id}>{p.name}</option>
        ))}
      </select>

      <select value={selectedDistrict} onChange={(e) => setSelectedDistrict(e.target.value)} disabled={!selectedProvince}>
        <option value="">Chọn Quận/Huyện</option>
        {districts.map(d => (
          <option key={d.id} value={d.id}>{d.name}</option>
        ))}
      </select>

      <select value={selectedWard} onChange={(e) => setSelectedWard(e.target.value)} disabled={!selectedDistrict}>
        <option value="">Chọn Xã/Phường</option>
        {wards.map(w => (
          <option key={w.id} value={w.id}>{w.name}</option>
        ))}
      </select>
    </div>
  );
}
```

### Vue.js Example

```vue
<template>
  <div>
    <select v-model="selectedProvince">
      <option value="">Chọn Tỉnh/Thành</option>
      <option v-for="p in provinces" :key="p.id" :value="p.id">
        {{ p.name }}
      </option>
    </select>

    <select v-model="selectedDistrict" :disabled="!selectedProvince">
      <option value="">Chọn Quận/Huyện</option>
      <option v-for="d in districts" :key="d.id" :value="d.id">
        {{ d.name }}
      </option>
    </select>

    <select v-model="selectedWard" :disabled="!selectedDistrict">
      <option value="">Chọn Xã/Phường</option>
      <option v-for="w in wards" :key="w.id" :value="w.id">
        {{ w.name }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const BASE_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api';

const provinces = ref([]);
const districts = ref([]);
const wards = ref([]);

const selectedProvince = ref('');
const selectedDistrict = ref('');
const selectedWard = ref('');

onMounted(async () => {
  const res = await fetch(`${BASE_URL}/provinces.json`);
  provinces.value = await res.json();
});

watch(selectedProvince, async (newVal) => {
  if (newVal) {
    const res = await fetch(`${BASE_URL}/districts/${newVal}.json`);
    districts.value = await res.json();
    selectedDistrict.value = '';
    wards.value = [];
  }
});

watch(selectedDistrict, async (newVal) => {
  if (newVal) {
    const res = await fetch(`${BASE_URL}/wards/${newVal}.json`);
    wards.value = await res.json();
    selectedWard.value = '';
  }
});
</script>
```

### Python

```python
import requests

BASE_URL = 'https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api'

# 1. Lấy tỉnh/thành
response = requests.get(f'{BASE_URL}/provinces.json')
provinces = response.json()

# 2. Lấy quận/huyện theo tỉnh
province_id = '11'  # Hà Nội
response = requests.get(f'{BASE_URL}/districts/{province_id}.json')
districts = response.json()

# 3. Lấy xã/phường theo quận
district_id = '267'  # Ba Đình
response = requests.get(f'{BASE_URL}/wards/{district_id}.json')
wards = response.json()

print(f"Tỉnh: {len(provinces)}")
print(f"Quận: {len(districts)}")
print(f"Xã: {len(wards)}")
```

---

## 📊 Cấu Trúc Dữ Liệu

### Province Object
```json
{
  "id": "11",
  "name": "Thành Phố Hà Nội",
  "new_id": "11",
  "new_name": "Thành Phố Hà Nội"
}
```

### District Object
```json
{
  "id": "267",
  "name": "Quận Ba Đình",
  "province_id": "11",
  "province_name": "Thành Phố Hà Nội",
  "new_province_id": "11",
  "new_province_name": "Thành Phố Hà Nội"
}
```

### Ward Object
```json
{
  "id": "65803",
  "name": "Phường Điện Biên",
  "district_id": "267",
  "district_name": "Quận Ba Đình",
  "province_id": "11",
  "province_name": "Thành Phố Hà Nội",
  "new_id": "14091",
  "new_name": "Phường Ba Đình",
  "new_province_id": "11",
  "new_province_name": "Thành Phố Hà Nội"
}
```

---

## 🎯 Use Cases

### 1. Form Đăng Ký/Đặt Hàng
```javascript
// Lưu địa chỉ đã chọn
const address = {
  province: provinces.find(p => p.id === selectedProvince),
  district: districts.find(d => d.id === selectedDistrict),
  ward: wards.find(w => w.id === selectedWard)
};

console.log(`${address.ward.name}, ${address.district.name}, ${address.province.name}`);
```

### 2. Tính Phí Ship Theo Khu Vực
```javascript
function calculateShippingFee(provinceId) {
  const specialProvinces = ['11', '12']; // HN, HCM
  return specialProvinces.includes(provinceId) ? 30000 : 50000;
}
```

### 3. Filter/Search Theo Địa Điểm
```javascript
// Tìm tất cả quận ở Hà Nội
const hanoiDistricts = await loadDistricts('11');
console.log(`Hà Nội có ${hanoiDistricts.length} quận/huyện`);
```

---

## � Lưu Ý

- **Cache dữ liệu**: Nên cache provinces.json vì ít thay đổi
- **Error handling**: Luôn xử lý lỗi khi fetch API
- **Loading state**: Hiển thị loading khi đang tải dữ liệu
- **Validation**: Kiểm tra user đã chọn đủ 3 cấp chưa

---

## � Links

- **Repository**: https://github.com/tanthuan031/vnadministrative
- **Demo**: Mở file `demo-api.html` để xem demo
