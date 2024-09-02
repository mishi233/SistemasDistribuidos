import { Component } from '@angular/core';
import { ApiService } from './api.service';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  nombres: string[] = [];
  nombreInput: string = "";
  nombreInput2: string = "";
  nombreMostrado: string = "";
  nombreEditando: string = ""; // Índice del nombre que se está editando

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.cargarNombres()
    
  }

  cargarNombres(){
    this.apiService.getNombres().subscribe(data => {
      this.nombres = data;
      this.nombreMostrado = this.nombres[Math.floor(Math.random() * this.nombres.length)];
    });
  }

  enviarNombre(): void {
    this.apiService.addNombre(this.nombreInput).subscribe(response => {
      this.nombres.push(this.nombreInput);
      this.nombreInput = "";
      console.log('Nombre enviado:', response);
      this.cargarNombres()
    });
  }

  editarNombre(index: number): void {
    this.nombreInput2 = this.nombres[index];
    this.nombreEditando = this.nombres[index];
  }

  guardarNombre(): void {
    if (this.nombreEditando !== null) {
      this.apiService.updateNombre(this.nombreEditando, this.nombreInput2).subscribe(response => {
        console.log('Nombre actualizado:', response);
        this.cargarNombres()
      });
    }
  }

  borrarNombre(index: number): void {
    this.apiService.deleteNombre(this.nombres[index]).subscribe(response => {
      console.log('Nombre borrado:', response);
      this.cargarNombres()
    });
  }
}
