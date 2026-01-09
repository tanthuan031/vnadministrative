#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chuyển đổi dữ liệu hành chính từ Excel sang 2 file JSON:
1. old_to_new.json - Tra cứu từ cũ sang mới
2. new_to_old.json - Tra cứu từ mới sang cũ
PHIÊN BẢN TỐI ƯU - Xử lý nhanh hơn
"""

import pandas as pd
import json
from collections import defaultdict


def create_mappings_optimized(df):
    """Tạo cả 2 mapping trong 1 lần duyệt dữ liệu - TỐI ƯU"""
    
    # Kết quả CŨ → MỚI
    old_to_new = {
        "metadata": {
            "title": "Mapping Hành Chính: Cũ → Mới",
            "description": "Tra cứu thông tin hành chính mới dựa trên thông tin cũ",
            "total_records": len(df)
        },
        "provinces": {},
        "districts": {},
        "wards": {}
    }
    
    # Kết quả MỚI → CŨ
    new_to_old = {
        "metadata": {
            "title": "Mapping Hành Chính: Mới → Cũ",
            "description": "Tra cứu thông tin hành chính cũ dựa trên thông tin mới",
            "total_records": len(df)
        },
        "provinces": {},
        "wards": {}
    }
    
    # Temporary storage
    provinces_old_seen = set()
    districts_old_seen = set()
    wards_old_seen = set()
    
    provinces_new_temp = defaultdict(lambda: {
        "new_province_id": "",
        "new_province_name": "",
        "old_provinces": [],
        "old_province_ids_seen": set()
    })
    
    wards_new_temp = defaultdict(lambda: {
        "new_ward_id": "",
        "new_ward_name": "",
        "new_province_id": "",
        "new_province_name": "",
        "old_wards": [],
        "old_ward_ids_seen": set()
    })
    
    print(f"   Đang xử lý {len(df)} dòng dữ liệu...")
    
    # Duyệt 1 lần duy nhất
    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"   Đã xử lý: {idx}/{len(df)} dòng...")
        
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
        
        # === TỈNH/THÀNH ===
        if province_id_old and province_id_old not in provinces_old_seen:
            # CŨ → MỚI
            old_to_new["provinces"][province_id_old] = {
                "old_province_id": province_id_old,
                "old_province_name": province_name_old,
                "new_province_id": province_id_new,
                "new_province_name": province_name_new
            }
            provinces_old_seen.add(province_id_old)
        
        # MỚI → CŨ (tỉnh)
        if province_id_new and province_id_old:
            temp = provinces_new_temp[province_id_new]
            temp["new_province_id"] = province_id_new
            temp["new_province_name"] = province_name_new
            
            if province_id_old not in temp["old_province_ids_seen"]:
                temp["old_provinces"].append({
                    "old_province_id": province_id_old,
                    "old_province_name": province_name_old
                })
                temp["old_province_ids_seen"].add(province_id_old)
        
        # === QUẬN/HUYỆN ===
        if district_id_old and district_id_old not in districts_old_seen:
            old_to_new["districts"][district_id_old] = {
                "old_district_id": district_id_old,
                "old_district_name": district_name_old,
                "old_province_id": province_id_old,
                "old_province_name": province_name_old,
                "new_province_id": province_id_new,
                "new_province_name": province_name_new,
                "note": "Quận/huyện cũ được sáp nhập vào tỉnh/thành mới"
            }
            districts_old_seen.add(district_id_old)
        
        # === XÃ/PHƯỜNG ===
        if ward_id_old and ward_id_old not in wards_old_seen:
            # CŨ → MỚI
            old_to_new["wards"][ward_id_old] = {
                "old_ward_id": ward_id_old,
                "old_ward_name": ward_name_old,
                "old_district_id": district_id_old,
                "old_district_name": district_name_old,
                "old_province_id": province_id_old,
                "old_province_name": province_name_old,
                "new_ward_id": ward_id_new,
                "new_ward_name": ward_name_new,
                "new_province_id": province_id_new,
                "new_province_name": province_name_new
            }
            wards_old_seen.add(ward_id_old)
        
        # MỚI → CŨ (xã)
        if ward_id_new and ward_id_old:
            temp = wards_new_temp[ward_id_new]
            temp["new_ward_id"] = ward_id_new
            temp["new_ward_name"] = ward_name_new
            temp["new_province_id"] = province_id_new
            temp["new_province_name"] = province_name_new
            
            if ward_id_old not in temp["old_ward_ids_seen"]:
                temp["old_wards"].append({
                    "old_ward_id": ward_id_old,
                    "old_ward_name": ward_name_old,
                    "old_district_id": district_id_old,
                    "old_district_name": district_name_old,
                    "old_province_id": province_id_old,
                    "old_province_name": province_name_old
                })
                temp["old_ward_ids_seen"].add(ward_id_old)
    
    print("   Đang hoàn thiện dữ liệu...")
    
    # Chuyển đổi provinces new_to_old
    for province_id, data in provinces_new_temp.items():
        new_to_old["provinces"][province_id] = {
            "new_province_id": data["new_province_id"],
            "new_province_name": data["new_province_name"],
            "old_provinces": data["old_provinces"],
            "total_old_provinces": len(data["old_provinces"])
        }
    
    # Chuyển đổi wards new_to_old
    for ward_id, data in wards_new_temp.items():
        new_to_old["wards"][ward_id] = {
            "new_ward_id": data["new_ward_id"],
            "new_ward_name": data["new_ward_name"],
            "new_province_id": data["new_province_id"],
            "new_province_name": data["new_province_name"],
            "old_wards": data["old_wards"],
            "total_old_wards": len(data["old_wards"])
        }
    
    return old_to_new, new_to_old


def main():
    excel_file = "admin_mapping_old_to_new_10_25.xlsx"
    
    print("📖 Đang đọc file Excel...")
    df = pd.read_excel(excel_file)
    print(f"✓ Đã đọc {len(df)} dòng dữ liệu\n")
    
    # Tạo cả 2 mapping cùng lúc
    print("🔄 Đang tạo mapping (tối ưu - chỉ duyệt 1 lần)...")
    old_to_new, new_to_old = create_mappings_optimized(df)
    
    # Lưu file
    print("\n💾 Đang lưu file old_to_new.json...")
    with open("old_to_new.json", 'w', encoding='utf-8') as f:
        json.dump(old_to_new, f, ensure_ascii=False, indent=2)
    print("✓ Đã tạo file: old_to_new.json")
    
    print("💾 Đang lưu file new_to_old.json...")
    with open("new_to_old.json", 'w', encoding='utf-8') as f:
        json.dump(new_to_old, f, ensure_ascii=False, indent=2)
    print("✓ Đã tạo file: new_to_old.json")
    
    print("\n" + "="*70)
    print("✅ HOÀN THÀNH!")
    print("="*70)
    
    print("\n📊 THỐNG KÊ FILE old_to_new.json:")
    print(f"   • Số tỉnh/thành cũ: {len(old_to_new['provinces'])}")
    print(f"   • Số quận/huyện cũ: {len(old_to_new['districts'])}")
    print(f"   • Số xã/phường cũ: {len(old_to_new['wards'])}")
    
    print("\n📊 THỐNG KÊ FILE new_to_old.json:")
    print(f"   • Số tỉnh/thành mới: {len(new_to_old['provinces'])}")
    print(f"   • Số xã/phường mới: {len(new_to_old['wards'])}")
    
    print("\n💡 CÁCH SỬ DỤNG:")
    print("\n1️⃣  File old_to_new.json - Tra cứu từ CŨ sang MỚI:")
    print("   • provinces[<id_tỉnh_cũ>] → thông tin tỉnh mới")
    print("   • districts[<id_quận_cũ>] → thông tin tỉnh mới (quận bị sáp nhập)")
    print("   • wards[<id_xã_cũ>] → thông tin xã mới")
    
    print("\n2️⃣  File new_to_old.json - Tra cứu từ MỚI sang CŨ:")
    print("   • provinces[<id_tỉnh_mới>] → danh sách tỉnh cũ")
    print("   • wards[<id_xã_mới>] → danh sách xã cũ")
    
    # Hiển thị ví dụ
    print("\n📝 VÍ DỤ:")
    if old_to_new['provinces']:
        first_province_id = list(old_to_new['provinces'].keys())[0]
        first_province = old_to_new['provinces'][first_province_id]
        print(f"\n   old_to_new.json → provinces['{first_province_id}']:")
        print(f"   {json.dumps(first_province, ensure_ascii=False, indent=6)}")
    
    if old_to_new['wards']:
        first_ward_id = list(old_to_new['wards'].keys())[0]
        first_ward = old_to_new['wards'][first_ward_id]
        print(f"\n   old_to_new.json → wards['{first_ward_id}']:")
        print(f"   {json.dumps(first_ward, ensure_ascii=False, indent=6)}")
    
    if new_to_old['wards']:
        first_ward_new_id = list(new_to_old['wards'].keys())[0]
        first_ward_new = new_to_old['wards'][first_ward_new_id]
        # Chỉ hiển thị 1 old_ward để ngắn gọn
        display_data = {
            "new_ward_id": first_ward_new["new_ward_id"],
            "new_ward_name": first_ward_new["new_ward_name"],
            "new_province_id": first_ward_new["new_province_id"],
            "new_province_name": first_ward_new["new_province_name"],
            "old_wards": first_ward_new["old_wards"][:1],
            "total_old_wards": first_ward_new["total_old_wards"]
        }
        if first_ward_new["total_old_wards"] > 1:
            display_data["note"] = f"... và {first_ward_new['total_old_wards'] - 1} xã cũ khác"
        
        print(f"\n   new_to_old.json → wards['{first_ward_new_id}']:")
        print(f"   {json.dumps(display_data, ensure_ascii=False, indent=6)}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
