/**
 * STUDENT MANAGEMENT SYSTEM - JAVASCRIPT CONTROLLER
 * Created for S. Vethavalli Portfolio Project
 */

document.addEventListener('DOMContentLoaded', () => {

  // ---------------------------------------------------------------------------
  // 1. Theme Toggle (Dark / Light)
  // ---------------------------------------------------------------------------
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const currentTheme = localStorage.getItem('sms-theme') || 'dark';

  if (currentTheme === 'light') {
    document.documentElement.classList.add('light-theme');
    if (themeToggleBtn) themeToggleBtn.textContent = '🌙';
  } else {
    document.documentElement.classList.remove('light-theme');
    if (themeToggleBtn) themeToggleBtn.textContent = '☀️';
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const isLight = document.documentElement.classList.toggle('light-theme');
      localStorage.setItem('sms-theme', isLight ? 'light' : 'dark');
      themeToggleBtn.textContent = isLight ? '🌙' : '☀️';
    });
  }

  // ---------------------------------------------------------------------------
  // 2. Mobile Sidebar Toggle
  // ---------------------------------------------------------------------------
  const mobileToggleBtn = document.getElementById('mobileToggleBtn');
  const sidebar = document.getElementById('sidebar');

  if (mobileToggleBtn && sidebar) {
    mobileToggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });
  }

  // ---------------------------------------------------------------------------
  // 3. Modal Opening & Closing Utilities
  // ---------------------------------------------------------------------------
  window.openModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('open');
      document.body.style.overflow = '';
    }
  };

  // Close modals when clicking background overlay or pressing Escape
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.open').forEach(modal => {
        modal.classList.remove('open');
      });
      document.body.style.overflow = '';
    }
  });

  // ---------------------------------------------------------------------------
  // 4. Edit Student Modal Pre-fill
  // ---------------------------------------------------------------------------
  window.populateEditStudentModal = function(id, roll, first, last, phone, dept, sem, gender) {
    const form = document.getElementById('editStudentForm');
    if (!form) return;

    form.action = `/students/edit/${id}`;
    document.getElementById('editRollNo').value = roll;
    document.getElementById('editFirstName').value = first;
    document.getElementById('editLastName').value = last;
    document.getElementById('editPhone').value = phone;
    document.getElementById('editDepartment').value = dept;
    document.getElementById('editSemester').value = sem;
    document.getElementById('editGender').value = gender;

    openModal('editStudentModal');
  };

  // ---------------------------------------------------------------------------
  // 5. Analytics Charts Initializer (Chart.js)
  // ---------------------------------------------------------------------------
  const gradeChartEl = document.getElementById('gradeDistributionChart');
  const deptChartEl = document.getElementById('deptDistributionChart');
  const subjectChartEl = document.getElementById('subjectAverageChart');
  const passFailChartEl = document.getElementById('passFailChart');

  if (gradeChartEl || deptChartEl || subjectChartEl || passFailChartEl) {
    fetch('/api/analytics-data')
      .then(res => res.json())
      .then(data => {
        // 1. Grade Distribution Chart (Bar)
        if (gradeChartEl) {
          new Chart(gradeChartEl, {
            type: 'bar',
            data: {
              labels: data.grades.labels,
              datasets: [{
                label: 'Student Count by Grade',
                data: data.grades.data,
                backgroundColor: [
                  '#10b981', '#14b8a6', '#06b6d4', '#3b82f6', '#8b5cf6', '#f59e0b', '#f43f5e'
                ],
                borderRadius: 6
              }]
            },
            options: {
              responsive: true,
              plugins: {
                legend: { display: false }
              },
              scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } }
              }
            }
          });
        }

        // 2. Department Breakdown Chart (Doughnut)
        if (deptChartEl) {
          new Chart(deptChartEl, {
            type: 'doughnut',
            data: {
              labels: data.departments.labels,
              datasets: [{
                data: data.departments.data,
                backgroundColor: ['#10b981', '#06b6d4', '#8b5cf6', '#f59e0b']
              }]
            },
            options: {
              responsive: true,
              plugins: {
                legend: { position: 'bottom' }
              }
            }
          });
        }

        // 3. Subject-wise Averages (Horizontal Bar)
        if (subjectChartEl) {
          new Chart(subjectChartEl, {
            type: 'bar',
            data: {
              labels: data.subjects.labels,
              datasets: [{
                label: 'Course Average (out of 100)',
                data: data.subjects.data,
                backgroundColor: '#06b6d4',
                borderRadius: 6
              }]
            },
            options: {
              indexAxis: 'y',
              responsive: true,
              scales: {
                x: { max: 100, beginAtZero: true }
              }
            }
          });
        }

        // 4. Pass vs Fail Ratio
        if (passFailChartEl) {
          new Chart(passFailChartEl, {
            type: 'pie',
            data: {
              labels: data.pass_fail.labels,
              datasets: [{
                data: data.pass_fail.data,
                backgroundColor: ['#10b981', '#f43f5e']
              }]
            },
            options: {
              responsive: true,
              plugins: {
                legend: { position: 'bottom' }
              }
            }
          });
        }
      })
      .catch(err => console.error('Error fetching analytics data:', err));
  }

});
