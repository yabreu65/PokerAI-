import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-prediction-modal',
  standalone: true,
  imports: [
    MatButtonModule,
  ],
  templateUrl: './prediction-modal.component.html',
  styleUrl: './prediction-modal.component.css'
})
export class PredictionModalComponent {
  @Input() predictionImage: string = '';
  @Input() prediction: string = '';
  @Output() close = new EventEmitter<void>();

  closeModal() {
    this.close.emit();
  }
}

