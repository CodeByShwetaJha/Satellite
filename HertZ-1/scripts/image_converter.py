import os
import base64
import json
from pathlib import Path
from datetime import datetime

def detailed_folder_scan():
    """Detailed scan to see exactly what's in your folders"""
    base_path = Path("C:/Users/skumari/OneDrive - Hexagon/Attachments/Project Satelite/HertZ-1/assets")
    sensors_path = base_path / "images" / "Sensors"
    
    print("🔍 DETAILED FOLDER SCAN")
    print("="*50)
    print(f"Looking in: {sensors_path}")
    
    if not sensors_path.exists():
        print("❌ Sensors folder NOT found!")
        return None
    
    print("✅ Sensors folder found!")
    
    # Get all subfolders
    folders = [f for f in sensors_path.iterdir() if f.is_dir()]
    print(f"📂 Found {len(folders)} subfolder(s):")
    
    folder_data = {}
    
    for folder in folders:
        print(f"\n📁 Scanning: {folder.name}")
        print(f"   Path: {folder}")
        
        # Get ALL files (not just images) to see what's there
        all_files = [f for f in folder.iterdir() if f.is_file()]
        
        # Separate by type
        images = []
        other_files = []
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tif'}
        
        for file in all_files:
            if file.suffix.lower() in image_extensions:
                images.append(file)
            else:
                other_files.append(file)
        
        print(f"   📸 Images: {len(images)}")
        if images:
            for img in sorted(images):
                size_kb = img.stat().st_size // 1024
                print(f"      • {img.name} ({size_kb}KB)")
        
        print(f"   📄 Other files: {len(other_files)}")
        if other_files:
            for file in sorted(other_files):
                print(f"      • {file.name}")
        
        # Check for subfolders
        subfolders = [f for f in folder.iterdir() if f.is_dir()]
        if subfolders:
            print(f"   📂 Subfolders: {len(subfolders)}")
            for subfolder in subfolders:
                print(f"      • {subfolder.name}/")
                # Check for images in subfolders too
                sub_images = []
                for ext in image_extensions:
                    sub_images.extend(subfolder.glob(f"*{ext}"))
                    sub_images.extend(subfolder.glob(f"*{ext.upper()}"))
                if sub_images:
                    print(f"        📸 {len(sub_images)} images in subfolder")
        
        folder_data[folder.name] = {
            'path': str(folder),
            'images': images,
            'subfolders': subfolders
        }
    
    return folder_data

def convert_images_to_base64(folder_data):
    """Convert your actual images to base64"""
    if not folder_data:
        return None
    
    print("\n" + "="*50)
    print("🔄 CONVERTING IMAGES TO BASE64")
    print("="*50)
    
    # Map your actual folders to gallery names
    folder_mapping = {
        'Sensarray-micro': 'sensarray',      # Your actual folder name
        'envirosense-pro': 'envirosense',    # Your actual folder name  
        'positiontrack-x2': 'positiontrack' # Your actual folder name
    }
    
    galleries = {}
    
    # MIME type mapping
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff',
        '.tif': 'image/tiff'
    }
    
    for actual_folder_name, folder_info in folder_data.items():
        # Get the gallery name for this folder
        gallery_name = folder_mapping.get(actual_folder_name, actual_folder_name.lower())
        
        print(f"\n🔄 Processing: {actual_folder_name} → {gallery_name}")
        
        images = folder_info['images']
        if not images:
            print("   ⚠️ No images found")
            continue
        
        print(f"   📸 Converting {len(images)} images...")
        
        base64_images = []
        
        for img_file in sorted(images, key=lambda x: x.name.lower()):
            try:
                print(f"      🔄 {img_file.name}", end="")
                
                # Read and encode image
                with open(img_file, "rb") as image_file:
                    image_data = image_file.read()
                    base64_encoded = base64.b64encode(image_data).decode('utf-8')
                    
                    # Get MIME type
                    file_ext = img_file.suffix.lower()
                    mime_type = mime_types.get(file_ext, 'image/jpeg')
                    
                    # Create data URI
                    data_uri = f"data:{mime_type};base64,{base64_encoded}"
                    base64_images.append(data_uri)
                    
                    size_kb = len(base64_encoded) // 1024
                    print(f" ✅ ({size_kb}KB base64)")
                    
            except Exception as e:
                print(f" ❌ Error: {e}")
        
        galleries[gallery_name] = {
            'current': 0,
            'images': base64_images
        }
        
        print(f"   ✅ {gallery_name}: {len(base64_images)} images converted")
    
    return galleries

def generate_javascript_file(galleries):
    """Generate the JavaScript file for your gallery"""
    if not galleries:
        print("❌ No galleries to generate")
        return
    
    base_path = Path("C:/Users/skumari/OneDrive - Hexagon/Attachments/Project Satelite/HertZ-1")
    scripts_path = base_path / "scripts"
    scripts_path.mkdir(exist_ok=True)
    
    js_content = f"""// AUTO-GENERATED BASE64 IMAGES
// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Source: Your images/Sensors/ folder
// 
// Folder mapping:
// • Sensarray-micro → sensarray
// • envirosense-pro → envirosense  
// • positiontrack-x2 → positiontrack

console.log('Loading your custom sensor images...');

// Your converted image galleries
const sensorGalleries = {json.dumps(galleries, indent=2)};

// Make available globally
window.sensorGalleries = sensorGalleries;

// Log success with detailed info
console.log('Custom sensor images loaded successfully!');
console.log('Gallery stats:');
Object.keys(sensorGalleries).forEach(key => {{
  console.log(`   ${{key}}: ${{sensorGalleries[key].images.length}} images`);
}});
"""
    
    js_file_path = scripts_path / "custom_images.js"
    with open(js_file_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"\n✅ JavaScript generated: {js_file_path}")
    
    # Generate integration instructions (without emojis to avoid Unicode issues)
    instructions = f"""
INTEGRATION INSTRUCTIONS:
================================

1. Add this line to your sensor_module.html (BEFORE your existing gallery script):
   <script src="../scripts/custom_images.js"></script>

2. Remove or comment out the old sensorGalleries object in your HTML

3. Your gallery will now have these products:
"""
    
    for gallery_name, gallery_data in galleries.items():
        instructions += f"   • {gallery_name}: {len(gallery_data['images'])} images\n"
    
    instructions += f"""
4. Update your HTML gallery sections to match these names:
   • sensarray (from Sensarray-micro folder)
   • envirosense (from envirosense-pro folder)  
   • positiontrack (from positiontrack-x2 folder)

Your existing JavaScript functions will work unchanged!
"""
    
    print(instructions)
    
    # Save instructions to file (with UTF-8 encoding)
    instructions_file = scripts_path / "integration_instructions.txt"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)

def main():
    """Main function"""
    print("🚀 HertZ Image Converter - DETAILED VERSION")
    
    # Step 1: Detailed scan
    folder_data = detailed_folder_scan()
    
    if not folder_data:
        input("\n❌ Press Enter to exit...")
        return
    
    # Step 2: Ask user to proceed
    print(f"\n{'='*50}")
    print("📋 SCAN COMPLETE!")
    print(f"{'='*50}")
    
    total_images = sum(len(info['images']) for info in folder_data.values())
    print(f"📊 Total images found: {total_images}")
    
    proceed = input(f"\n🤔 Convert {total_images} images to base64? (y/n): ").lower().strip()
    
    if proceed != 'y':
        print("👋 Conversion cancelled")
        input("Press Enter to exit...")
        return
    
    # Step 3: Convert images
    galleries = convert_images_to_base64(folder_data)
    
    if not galleries:
        print("❌ No images converted")
        input("Press Enter to exit...")
        return
    
    # Step 4: Generate JavaScript
    generate_javascript_file(galleries)
    
    print(f"\n{'='*50}")
    print("🎉 CONVERSION COMPLETE!")
    print(f"{'='*50}")
    
    input("\n✅ Press Enter to close...")

if __name__ == "__main__":
    main()