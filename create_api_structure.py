#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo cấu trúc API theo từng cấp
Tạo các file JSON riêng biệt cho provinces, districts, wards
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict


def create_api_structure(df):
    """Tạo cấu trúc API theo từng cấp"""
    
    # Tạo thư mục
    api_dir = Path("api")
    api_dir.mkdir(exist_ok=True)
    
    districts_dir = api_dir / "districts"
    districts_dir.mkdir(exist_ok=True)
    
    wards_dir = api_dir / "wards"
    wards_dir.mkdir(exist_ok=True)
    
    # Storage
    provinces_data = {}
    districts_by_province = defaultdict(dict)
    wards_by_district = defaultdict(dict)
    
    print("Đang xử lý dữ liệu...")
    
    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"  Đã xử lý: {idx}/{len(df)} dòng...")
        
        # Lấy dữ liệu
        province_id_old = str(int(row['city_id_old'])) if pd.notna(row['city_id_old']) else None
        province_name_old = str(row['city_name_old']).strip() if pd.notna(row['city_name_old']) else None
        district_id_old = str(int(row['district_id_old'])) if pd.notna(row['district_id_old']) else None
        district_name_old = str(row['district_name_old']).strip() if pd.notna(row['district_name_old']) else None
        ward_id_old = str(int(row['ward_id_old'])) if pd.notna(row['ward_id_old']) else None
        ward_name_old = str(row['ward_name_old']).strip() if pd.notna(row['ward_name_old']) else None
        
        province_id_new = str(int(row['city_id_new'])) if pd.notna(row['city_id_new']) else None
        province_name_new = str(row['city_name_new']).strip() if pd.notna(row['city_name_new']) else None
        ward_id_new = str(int(row['ward_id_new'])) if pd.notna(row['ward_id_new']) else None
        ward_name_new = str(row['ward_new_name']).strip() if pd.notna(row['ward_new_name']) else None
        
        # PROVINCES
        if province_id_old and province_id_old not in provinces_data:
            provinces_data[province_id_old] = {
                "id": province_id_old,
                "name": province_name_old,
                "new_id": province_id_new,
                "new_name": province_name_new
            }
        
        # DISTRICTS by Province
        if district_id_old and district_id_old not in districts_by_province[province_id_old]:
            districts_by_province[province_id_old][district_id_old] = {
                "id": district_id_old,
                "name": district_name_old,
                "province_id": province_id_old,
                "province_name": province_name_old,
                "new_province_id": province_id_new,
                "new_province_name": province_name_new
            }
        
        # WARDS by District
        if ward_id_old and ward_id_old not in wards_by_district[district_id_old]:
            wards_by_district[district_id_old][ward_id_old] = {
                "id": ward_id_old,
                "name": ward_name_old,
                "district_id": district_id_old,
                "district_name": district_name_old,
                "province_id": province_id_old,
                "province_name": province_name_old,
                "new_id": ward_id_new,
                "new_name": ward_name_new,
                "new_province_id": province_id_new,
                "new_province_name": province_name_new
            }
    
    print("\nĐang tạo files...")
    
    # 1. Tạo provinces.json
    provinces_list = list(provinces_data.values())
    with open(api_dir / "provinces.json", 'w', encoding='utf-8') as f:
        json.dump(provinces_list, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã tạo: api/provinces.json ({len(provinces_list)} tỉnh)")
    
    # 2. Tạo districts/{province_id}.json
    for province_id, districts in districts_by_province.items():
        districts_list = list(districts.values())
        with open(districts_dir / f"{province_id}.json", 'w', encoding='utf-8') as f:
            json.dump(districts_list, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã tạo: {len(districts_by_province)} files trong api/districts/")
    
    # 3. Tạo wards/{district_id}.json
    for district_id, wards in wards_by_district.items():
        wards_list = list(wards.values())
        with open(wards_dir / f"{district_id}.json", 'w', encoding='utf-8') as f:
            json.dump(wards_list, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã tạo: {len(wards_by_district)} files trong api/wards/")
    
    return {
        "provinces_count": len(provinces_list),
        "districts_count": len(districts_by_province),
        "wards_count": len(wards_by_district)
    }


def main():
    excel_file = "admin_mapping_old_to_new_10_25.xlsx"
    
    print("📖 Đang đọc file Excel...")
    df = pd.read_excel(excel_file)
    print(f"✓ Đã đọc {len(df)} dòng dữ liệu\n")
    
    stats = create_api_structure(df)
    
    print("\n" + "="*70)
    print("✅ HOÀN THÀNH!")
    print("="*70)
    
    print("\n📊 THỐNG KÊ:")
    print(f"   • Số tỉnh/thành: {stats['provinces_count']}")
    print(f"   • Số file quận/huyện: {stats['districts_count']}")
    print(f"   • Số file xã/phường: {stats['wards_count']}")
    
    print("\n📁 CẤU TRÚC THƯ MỤC:")
    print("   api/")
    print("   ├── provinces.json")
    print("   ├── districts/")
    print("   │   ├── 11.json (Hà Nội)")
    print("   │   ├── 12.json (Hải Phòng)")
    print("   │   └── ...")
    print("   └── wards/")
    print("       ├── 267.json (Ba Đình)")
    print("       ├── 268.json (Hoàn Kiếm)")
    print("       └── ...")
    
    print("\n💡 CÁCH SỬ DỤNG:")
    print("\n1️⃣  Lấy danh sách tỉnh:")
    print("   GET api/provinces.json")
    
    print("\n2️⃣  Lấy danh sách quận/huyện theo tỉnh:")
    print("   GET api/districts/{province_id}.json")
    print("   Ví dụ: api/districts/11.json (Hà Nội)")
    
    print("\n3️⃣  Lấy danh sách xã/phường theo quận:")
    print("   GET api/wards/{district_id}.json")
    print("   Ví dụ: api/wards/267.json (Ba Đình)")
    
    print("\n🌐 URL trên GitHub (sau khi push):")
    print("   https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/provinces.json")
    print("   https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/districts/11.json")
    print("   https://raw.githubusercontent.com/tanthuan031/vnadministrative/main/api/wards/267.json")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
