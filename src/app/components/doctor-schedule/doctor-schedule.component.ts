import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-doctor-schedule',
  template: `
    <div class="schedule-container">
      <div class="header">
        <h2><i class="fas fa-calendar"></i> Gestion des Horaires Médecins</h2>
        <button class="btn btn-primary" (click)="showAddForm = true">
          <i class="fas fa-plus"></i> Ajouter un horaire
        </button>
      </div>
      
      <div class="doctors-list">
        <div class="doctor-card" *ngFor="let doctor of doctors">
          <div class="doctor-header">
            <h4>{{doctor.user?.prenom}} {{doctor.user?.nom}}</h4>
            <span class="specialty">{{doctor.specialite}}</span>
          </div>
          <div class="schedule-info">
            <p><strong>Téléphone:</strong> {{doctor.telephone || 'Non renseigné'}}</p>
            <p><strong>Horaires:</strong> {{doctor.horaires || 'Non définis'}}</p>
            <p><strong>Statut:</strong> 
              <span class="badge" [ngClass]="doctor.is_active ? 'badge-success' : 'badge-danger'">
                {{doctor.is_active ? 'Actif' : 'Inactif'}}
              </span>
            </p>
          </div>
          <div class="actions">
            <button class="btn btn-sm btn-primary" (click)="editSchedule(doctor)">
              <i class="fas fa-edit"></i> Modifier
            </button>
            <button class="btn btn-sm btn-warning" (click)="viewSchedule(doctor)">
              <i class="fas fa-calendar"></i> Voir horaires
            </button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .schedule-container {
      margin-left: 250px;
      padding: 20px;
    }
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 2px solid #e9ecef;
    }
    
    .header h2 {
      color: #2c3e50;
      margin: 0;
    }
    
    .doctors-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 20px;
    }
    
    .doctor-card {
      background: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .doctor-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }
    
    .doctor-header h4 {
      margin: 0;
      color: #2c3e50;
    }
    
    .specialty {
      background: #3498db;
      color: white;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
    }
    
    .schedule-info p {
      margin: 10px 0;
      color: #6c757d;
    }
    
    .actions {
      display: flex;
      gap: 10px;
      margin-top: 15px;
    }
    
    .btn {
      padding: 8px 16px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }
    
    .btn-primary {
      background: #007bff;
      color: white;
    }
    
    .btn-warning {
      background: #ffc107;
      color: black;
    }
    
    .btn-sm {
      padding: 4px 8px;
      font-size: 12px;
    }
    
    .badge {
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
    }
    
    .badge-success {
      background: #28a745;
      color: white;
    }
    
    .badge-danger {
      background: #dc3545;
      color: white;
    }
  `]
})
export class DoctorScheduleComponent implements OnInit {
  doctors: any[] = [];
  showAddForm = false;
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.loadDoctors();
  }
  
  loadDoctors() {
    this.http.get('/api/admin/doctors').subscribe(
      (data: any[]) => {
        this.doctors = data;
      },
      (error) => {
        console.error('Error loading doctors:', error);
      }
    );
  }
  
  editSchedule(doctor: any) {
    console.log('Editing schedule for:', doctor);
  }
  
  viewSchedule(doctor: any) {
    console.log('Viewing schedule for:', doctor);
  }
}