import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, HttpClientModule],  // Asegúrate de que CommonModule esté aquí
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'ia-angular';
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  prediction: string | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.startCamera();
  }

  startCamera() {
    const video = document.getElementById('video') as HTMLVideoElement;

    // Configuración para intentar usar la cámara trasera en móviles
    const constraints = {
      video: { facingMode: "environment" } 
    };

    navigator.mediaDevices.getUserMedia(constraints)
      .then((stream) => {
        video.srcObject = stream;
      })
      .catch((error) => {
        console.error('Error al acceder a la cámara:', error);
      });
  }
  captureImage() {
    const video = document.getElementById('video') as HTMLVideoElement;
    const canvas = document.getElementById('canvas') as HTMLCanvasElement;
    const context = canvas.getContext('2d');

    if (context) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.previewUrl = canvas.toDataURL('image/png');
      this.selectedFile = this.dataUrlToFile(this.previewUrl, 'captured-image.png');
    }
  }


  dataUrlToFile(dataUrl: string, filename: string): File {
    const arr = dataUrl.split(',');
    const mime = arr[0].match(/:(.*?);/)![1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, { type: mime });
  }

  onFileChange(event: any) {
    const file = event.target.files[0];
    this.selectedFile = file;

    const reader = new FileReader();
    reader.onload = () => {
      this.previewUrl = reader.result as string;
    };
    reader.readAsDataURL(file);
  }

  uploadImage() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);

    this.http.post<any>('http://localhost:5001/predict', formData).subscribe(
      (response: any) => {
        this.prediction = response.prediction;
        console.log("Predicción recibida:", response);
      },
      (error: any) => {
        console.error('Error al predecir:', error);
      }
    );
  }
}
