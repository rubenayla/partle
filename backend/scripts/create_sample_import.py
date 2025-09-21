#!/usr/bin/env python3
"""
Create sample CSV and Excel import templates for bulk product upload.
"""
import pandas as pd
import os

# Sample product data
sample_data = {
    'sku': [
        'LAPTOP-001',
        'MOUSE-WL-02',
        'KB-MECH-RGB',
        'HUB-USBC-01',
        'STAND-MON-ADJ',
        'CAM-HD-1080',
        'HEADSET-PRO',
        'SSD-EXT-1TB',
        'CABLE-MGT-01',
        'COOL-PAD-01'
    ],
    'name': [
        'Gaming Laptop Pro X1',
        'Wireless Ergonomic Mouse',
        'Mechanical RGB Keyboard',
        'USB-C Multiport Hub',
        'Adjustable Monitor Stand',
        'Webcam HD 1080p',
        'Wireless Headset Pro',
        'External SSD 1TB',
        'Cable Management Kit',
        'Laptop Cooling Pad'
    ],
    'price': [
        1299.99,
        29.99,
        89.99,
        49.99,
        39.99,
        79.99,
        119.99,
        149.99,
        19.99,
        34.99
    ],
    'description': [
        'High-performance gaming laptop with RTX 4060 graphics, 16GB RAM, 512GB SSD',
        'Ergonomic wireless mouse with 3-year battery life and precision tracking',
        'RGB mechanical keyboard with customizable backlighting and blue switches',
        'Multi-port USB-C hub with HDMI 4K, ethernet, and 100W power delivery',
        'Height-adjustable monitor stand with built-in cable management system',
        'Full HD webcam with auto-focus, noise cancellation, and privacy shutter',
        'Professional wireless headset with active noise cancellation',
        'Portable external SSD with USB-C, 1000MB/s transfer speed',
        'Complete cable management solution with clips, sleeves, and ties',
        'Laptop cooling pad with 5 quiet fans and adjustable height'
    ],
    'url': [
        'https://example.com/products/gaming-laptop-x1',
        'https://example.com/products/wireless-mouse',
        'https://example.com/products/rgb-keyboard',
        'https://example.com/products/usbc-hub',
        'https://example.com/products/monitor-stand',
        'https://example.com/products/webcam-hd',
        'https://example.com/products/wireless-headset',
        'https://example.com/products/ssd-1tb',
        'https://example.com/products/cable-kit',
        'https://example.com/products/cooling-pad'
    ],
    'image': [
        'laptop.jpg',
        'mouse.jpg',
        'keyboard.jpg',
        'hub.jpg',
        'stand.jpg',
        'webcam.jpg',
        'headset.jpg',
        'ssd.jpg',
        'cables.jpg',
        'cooling.jpg'
    ],
    'tags': [
        'electronics,gaming,computers,laptops',
        'electronics,accessories,peripherals',
        'electronics,gaming,accessories,keyboards',
        'electronics,accessories,adapters',
        'office,accessories,ergonomics',
        'electronics,webcams,video',
        'electronics,audio,headphones',
        'electronics,storage,portable',
        'office,accessories,organization',
        'electronics,accessories,cooling'
    ]
}

# Create DataFrame with columns in logical order
column_order = ['sku', 'name', 'price', 'description', 'url', 'image', 'tags']
df = pd.DataFrame(sample_data)[column_order]

# Create output directory
output_dir = 'sample_imports'
os.makedirs(output_dir, exist_ok=True)

# Save as CSV
csv_path = os.path.join(output_dir, 'product_import_template.csv')
df.to_csv(csv_path, index=False)
print(f"✅ Created CSV template: {csv_path}")

# Save as Excel with formatting
excel_path = os.path.join(output_dir, 'product_import_template.xlsx')
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Products', index=False)

    # Get the workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets['Products']

    # Add column widths
    column_widths = {
        'A': 25,  # name
        'B': 10,  # price
        'C': 60,  # description
        'D': 40,  # url
        'E': 15,  # image
        'F': 30,  # tags
    }

    for col, width in column_widths.items():
        worksheet.column_dimensions[col].width = width

    # Add instructions sheet
    instructions_df = pd.DataFrame({
        'Column': ['sku', 'name', 'price', 'description', 'url', 'image', 'tags'],
        'Required': ['No', 'Yes', 'Yes', 'No', 'No', 'No', 'No'],
        'Description': [
            'Stock Keeping Unit - unique per store (text, optional)',
            'Product name (text)',
            'Product price (number, e.g., 29.99)',
            'Product description (text, optional)',
            'Product URL/link (text, optional)',
            'Image filename from ZIP (e.g., product.jpg)',
            'Comma-separated tags (e.g., electronics,gaming)'
        ],
        'Example': [
            'LAPTOP-001',
            'Gaming Laptop Pro',
            '1299.99',
            'High-performance laptop with RTX graphics',
            'https://example.com/laptop',
            'laptop.jpg',
            'electronics,gaming,computers'
        ]
    })

    instructions_df.to_excel(writer, sheet_name='Instructions', index=False)

    # Format instructions sheet
    instructions_sheet = writer.sheets['Instructions']
    instructions_sheet.column_dimensions['A'].width = 15
    instructions_sheet.column_dimensions['B'].width = 12
    instructions_sheet.column_dimensions['C'].width = 50
    instructions_sheet.column_dimensions['D'].width = 40

print(f"✅ Created Excel template: {excel_path}")

# Create a minimal CSV for quick testing
minimal_data = {
    'name': ['Test Product 1', 'Test Product 2', 'Test Product 3'],
    'price': [9.99, 19.99, 29.99]
}
minimal_df = pd.DataFrame(minimal_data)
minimal_path = os.path.join(output_dir, 'minimal_import.csv')
minimal_df.to_csv(minimal_path, index=False)
print(f"✅ Created minimal CSV template: {minimal_path}")

print(f"\n📁 All templates saved in: {os.path.abspath(output_dir)}/")
print("\n📋 Instructions for use:")
print("1. Fill in product details in the template file")
print("2. Required fields: 'name' and 'price'")
print("3. Optional: Add image filenames and create a ZIP with those images")
print("4. Upload both files through the Partle bulk import interface")