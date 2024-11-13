import {  CommonModule } from '@angular/common';
import { Component, ViewChild, ElementRef, AfterViewInit, HostListener, OnInit, ChangeDetectorRef} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import * as QRCode from 'qrcode';
import { PredictionModalComponent } from './prediction-modal/prediction-modal.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    PredictionModalComponent,
    CommonModule,
    MatToolbarModule,
    MatCardModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
    MatButtonModule,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, AfterViewInit {
  isMobile = false;
  showModal = false;
  predictionImage = '';
  prediction = '';
  
  @ViewChild('fileInput') fileInput!: ElementRef;
  @ViewChild('video', { static: false }) videoElementRef!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvas', { static: false }) canvasElementRef!: ElementRef<HTMLCanvasElement>;
  

  showVideo = true;
  showCanvas = false;
  
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  cardImage = '';
  qrCodeUrl = `${environment.desktopUrl}`;
  qrCodeImage = '';

  cards: string[] = [
    '2H.png', '3H.png', '4H.png', '5H.png', '6H.png', '7H.png', '8H.png', '9H.png', '10H.png', 'JH.png', 'QH.png', 'KH.png', 'AH.png',
    '2D.png', '3D.png', '4D.png', '5D.png', '6D.png', '7D.png', '8D.png', '9D.png', '10D.png', 'JD.png', 'QD.png', 'KD.png', 'AD.png',
    '2C.png', '3C.png', '4C.png', '5C.png', '6C.png', '7C.png', '8C.png', '9C.png', '10C.png', 'JC.png', 'QC.png', 'KC.png', 'AC.png',
    '2S.png', '3S.png', '4S.png', '5S.png', '6S.png', '7S.png', '8S.png', '9S.png', '10S.png', 'JS.png', 'QS.png', 'KS.png', 'AS.png'
  ];

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.detectDevice();
    this.generateQRCode(this.qrCodeUrl);
  }

  ngAfterViewInit() {
    this.loadRandomCard();
    this.generateQRCode(this.qrCodeUrl);
    this.detectDevice();
 
    // Añade un breve retraso para dispositivos móviles
    setTimeout(() => {
      console.log("Intentando iniciar la cámara...");
      this.startCamera(this.videoElementRef); // Pasa el videoElementRef aquí
    }, 500); // Ajusta el tiempo si es necesario
  }
  

  @HostListener('window:resize', [])
  detectDevice() {
    this.isMobile = window.innerWidth <= 768;
    this.cdr.detectChanges(); 
    console.log('Device type:', this.isMobile ? 'Mobile' : 'Desktop');
  }
  
  generateQRCode(url: string) {
    QRCode.toDataURL(url, (err: any, url: string) => {
      if (err) {
        console.error('Error al generar QR:', err);
        return;
      }
      this.qrCodeImage = url;
    });
  }

  startCamera(videoElementRef: ElementRef<HTMLVideoElement>) {
    if (!videoElementRef) {
      console.error("El elemento de video no está disponible en startCamera.");
      return;
    }
  
    const videoElement = videoElementRef.nativeElement;
    const tryFrontCamera = { video: { facingMode: "user" } };
    const tryBackCamera = { video: { facingMode: "environment" } };
  
    console.log("Iniciando cámara en el dispositivo...");
  
    navigator.mediaDevices.getUserMedia(tryFrontCamera)
      .then((stream) => {
        videoElement.srcObject = stream;
        this.showVideo = true;
        this.showCanvas = false;
        console.log("Cámara frontal iniciada con éxito.");
      })
      .catch((error) => {
        console.warn("Cámara frontal no disponible, intentando con cámara trasera:", error);
        navigator.mediaDevices.getUserMedia(tryBackCamera)
          .then((stream) => {
            videoElement.srcObject = stream;
            this.showVideo = true;
            this.showCanvas = false;
            console.log("Cámara trasera iniciada con éxito.");
          })
          .catch((err) => {
            console.error("Error al intentar acceder a cualquier cámara:", err);
          });
      });
  }

  loadRandomCard() {
    const randomIndex = Math.floor(Math.random() * this.cards.length);
    this.cardImage = `assets/images/${this.cards[randomIndex]}`;
  }

  selectCard(event: any) {
    this.cardImage = `assets/images/${event.value}`;
  }

  captureImage() {
    console.log("Capturando imagen...");
    this.showCanvas = true;
  
    setTimeout(() => {
  const videoElement = this.videoElementRef.nativeElement;
  const canvasElement = this.canvasElementRef.nativeElement;
  const captureAreaElement = document.getElementById('captureArea');

  if (videoElement && canvasElement && captureAreaElement) {
    const videoRect = videoElement.getBoundingClientRect();
    const captureRect = captureAreaElement.getBoundingClientRect();

    const scaleX = videoElement.videoWidth / videoRect.width;
    const scaleY = videoElement.videoHeight / videoRect.height;

    const sx = (captureRect.left - videoRect.left) * scaleX;
    const sy = (captureRect.top - videoRect.top) * scaleY;
    const sw = captureRect.width * scaleX;
    const sh = captureRect.height * scaleY;

    canvasElement.width = sw;
    canvasElement.height = sh;

    const context = canvasElement.getContext('2d');
    if (context) {
      context.drawImage(videoElement, sx, sy, sw, sh, 0, 0, sw, sh);
      canvasElement.toBlob((blob) => {
        if (blob) {
          this.selectedFile = new File([blob], 'captured-image.png', { type: 'image/png' });
          this.uploadImage();
        }
      }, 'image/png');
    }
  } else {
    console.error('Los elementos de video o canvas no están disponibles.');
  }
  this.showVideo = false;
  this.showCanvas = true;

    }, 500);
  }
  
  // Método para manejar el cambio en la selección de archivo
  triggerFileInput() {
    // Simula un clic en el input de tipo file
    this.fileInput.nativeElement.click();
  }
  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  uploadImage() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);

    this.http.post<any>(`${environment.apiUrl}/predict`, formData).subscribe(
      (response: any) => {
        this.prediction = this.transformPredictionToImage(response.prediction);
        this.predictionImage = `assets/images/${this.prediction}.png`;
        this.showModal = true;
        this.cdr.detectChanges();
      },
      (error: any) => {
        console.error('Error al predecir:', error);
      }
    );
  }

  handleModalClose() {
    this.showModal = false;
    location.reload();
  }

  private transformPredictionToImage(prediction: string): string {
    return prediction.split('_').pop() || '';
  }
}
