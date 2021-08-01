# Double JPEG Detection
2021 인하대학교 컴퓨터공학종합설계 프로젝트<br>
9조 최희정, 서민균, 양유진<br>


## **About the Project**
<hr/>
Single Compressed JPEG과 Double Compressed JPEG을 구분하여 합성 영역을 Localization 한다.<br>
<i>Double JPEG Detection in Mixed JPEG Quality Factors using Deep Convolutional Neural Network</i>

[논문](https://openaccess.thecvf.com/content_ECCV_2018/papers/Jin-Seok_Park_Double_JPEG_Detection_ECCV_2018_paper.pdf)([GitHub](https://github.com/plok5308/DJPEG-torch))에서 제공하는 Quantization table을 이용하여 Sinlge Compressed JPEG, Double Compressed JPEG 데이터셋을 생성하였다. <br><br><br>

### **Built With**
- 사용 언어: 파이썬
  - [pytorch](https://github.com/pytorch/pytorch)
  - [PIL](https://github.com/python-pillow/Pillow)
  - [numpy](https://github.com/numpy/numpy)
  - [matplotlib](https://github.com/matplotlib/matplotlib)
  - [pandas](https://github.com/pandas-dev/pandas)

## **Getting Started**
<hr/>

### **Requirements**
```
pip install torch
pip install pillow
pip install numpy
pip install matplotlib
```

### **Dataset**
데이터셋 다운로드는 [여기](https://drive.google.com/file/d/1aZoD8dPIVgEWdpA8szctypjO-tcD6m0S/view?usp=sharing)

### **Models**
Localization에 사용한 네 개의 모델 다운로드 링크<br>
[Net1](https://drive.google.com/file/d/1q8wHtLn90oU1xIhJ4J15N28TLl8KHDhr/view?usp=sharing), [Net2](https://drive.google.com/file/d/1XahWLqU9eqBVM7DQYp6EuYwkzM_kzCLA/view?usp=sharing), [Net3](https://drive.google.com/file/d/1zl_Vj3e3SUfHHlkvwob_5J6E623Rvd_S/view?usp=sharing), [Net4](https://drive.google.com/file/d/15RVnLhpNNpPan2i6fsnzfvJL8dSHT_QY/view?usp=sharing)<br>

각 모델에서 사용한 파라미터 리스트<br>
| Network | Conv1D-a | Conv1D-b | Bin range | Bidirectional | AC/DC |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|Net1|kernel size = 7|kernel size = 7|[-80, 80]|X|AC Only|
|Net2|kernel size = 5|kernel size = 5|[-60, -60]|X|AC Only|
|Net3|kernel size = 7|kernel size = 5|[-60, 60]|O|AC Only|
|Net4|kernel size = 5|kernel size = 5|[-60, 60]|O|AC and DC|<br>

## **Additional Info**
추가적인 내용은 Final_Report.docx 파일과
test_files/colab link + 실행 방법 파일 참고