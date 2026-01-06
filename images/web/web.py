import os
from PIL import Image

def convert_png_to_webp(quality=80, lossless=False):
    """
    현재 디렉토리의 모든 PNG 파일을 WebP로 변환합니다.
    
    :param quality: 웹피 이미지 품질 (0~100). 기본값 80.
    :param lossless: 무손실 압축 여부 (True/False). True일 경우 품질 설정 무시.
    """
    
    # 현재 작업 경로
    current_dir = os.getcwd()
    
    # 결과물을 저장할 폴더 생성
    output_dir = os.path.join(current_dir, "converted_webp")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 변환 작업 시작
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.png')]
    
    if not files:
        print("현재 폴더에 .png 파일이 없습니다.")
        return

    print(f"총 {len(files)}개의 PNG 파일을 발견했습니다. 변환을 시작합니다...\n")

    for filename in files:
        try:
            # 이미지 열기
            img_path = os.path.join(current_dir, filename)
            image = Image.open(img_path)

            # 파일명에서 확장자 제거 및 경로 설정
            file_name_without_ext = os.path.splitext(filename)[0]
            save_path = os.path.join(output_dir, f"{file_name_without_ext}.webp")

            # WebP로 저장
            # RGBA(투명 배경)도 WebP는 지원하므로 모드 변경 불필요
            image.save(save_path, 'webp', quality=quality, lossless=lossless)
            
            print(f"[완료] {filename} -> {file_name_without_ext}.webp")
            
        except Exception as e:
            print(f"[실패] {filename}: {e}")

    print(f"\n변환이 완료되었습니다! 결과물은 '{output_dir}' 폴더를 확인하세요.")

if __name__ == "__main__":
    # 사용 설정
    # quality: 1~100 사이 (보통 80 정도가 용량 대비 화질이 좋음)
    # lossless: True로 하면 무손실 압축 (용량은 좀 더 큼), False면 손실 압축
    convert_png_to_webp(quality=80, lossless=False)