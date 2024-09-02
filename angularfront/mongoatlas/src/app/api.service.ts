import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8000/nombres'; // URL de FastAPI

  constructor(private http: HttpClient) { }

  // Obtener todos los nombres
  getNombres(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/obtener`);
  }

  // Añadir un nuevo nombre
  addNombre(nombre: string): Observable<string> {
    return this.http.post<string>(`${this.apiUrl}/agregar`, { nombre });
  }

  // Actualizar un nombre existente por su nombre actual
  updateNombre(nombreActual: string, nuevoNombre: string): Observable<string> {
    return this.http.put<string>(`${this.apiUrl}/actualizar`, {nombreActual,  nuevoNombre});
  }

  // Borrar un nombre por su valor
  deleteNombre(nombre: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/borrar/${nombre}`);
  }
}
