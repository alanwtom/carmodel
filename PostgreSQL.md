### **Migration Plan for PostgreSQL Database**

#### **1. Database Setup**

**1.1. Current Database:**

* The current setup is using SQLite (`sqlite:///travora.db`).
* The new database should be PostgreSQL (`postgresql://user:password@localhost/travora`).

**1.2. Install PostgreSQL and psycopg2:**

* Ensure that PostgreSQL is installed on your system.
* Install `psycopg2`, the PostgreSQL adapter for Python:

  ```bash
  pip install psycopg2
  ```

**1.3. Update Environment Variables:**

* Update `.env` file with PostgreSQL database URI:

  ```plaintext
  DATABASE_URL=postgresql://username:password@localhost/travora
  SECRET_KEY=your-secret-key
  ```

#### **2. Code Changes**

**2.1. Update `app.py`:**

* Replace the SQLite URI with the PostgreSQL URI from `.env` file:

  ```python
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
  ```

#### **3. Migration Process**

**3.1. Using Flask-Migrate for Database Migration:**
Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask apps using Alembic.

* Install Flask-Migrate:

  ```bash
  pip install flask-migrate
  ```

* In `app.py`, initialize Flask-Migrate:

  ```python
  from flask_migrate import Migrate

  migrate = Migrate(app, db)
  ```

**3.2. Initialize Alembic:**
Run the following command to set up Alembic for migrations:

```bash
flask db init
```

This will create a `migrations` folder in your project.

**3.3. Generate Migration Scripts:**
To create migration scripts based on the current database schema, run:

```bash
flask db migrate -m "Initial migration"
```

**3.4. Apply Migrations to PostgreSQL:**
Once the migration scripts are generated, you can apply the migrations to your PostgreSQL database:

```bash
flask db upgrade
```

#### **4. Data Migration**

**4.1. Migrate Existing Data from SQLite to PostgreSQL:**

* If you're moving from SQLite to PostgreSQL and already have data in your SQLite database, use a database migration tool or custom scripts to migrate the data.
* You can also dump the SQLite data and import it into PostgreSQL using the following steps:

  * Export data from SQLite:

    ```bash
    sqlite3 travora.db .dump > dump.sql
    ```
  * Modify the dump file if necessary (remove SQLite-specific statements, and make adjustments for PostgreSQL compatibility).
  * Import the data into PostgreSQL:

    ```bash
    psql -h localhost -U username -d travora -f dump.sql
    ```

#### **5. Testing and Verification**

**5.1. Testing the Migration:**

* Verify that the application works with the new PostgreSQL database by running the app locally and performing basic operations like user registration, login, and booking.
* Check for any issues related to data integrity and queries.

**5.2. Handling Any Issues:**

* PostgreSQL has some differences from SQLite, especially with data types and constraints, so ensure the schema is compatible and adjust queries or data types as necessary.

#### **6. Rollback Plan**

**6.1. Backup Database:**
Before migrating, ensure a full backup of the SQLite database is taken.

**6.2. Rollback:**
If the migration fails or introduces issues, you can revert back to SQLite by:

* Restoring the backup of SQLite.
* Changing the `SQLALCHEMY_DATABASE_URI` back to the SQLite URI in `app.py`.

---

### **Post-Migration Steps**

#### **7. Final Checks**

**7.1. Test All Features:**

* Test all features of the application to ensure data consistency, and that queries work properly with PostgreSQL.

**7.2. Monitor Performance:**

* PostgreSQL typically performs better with larger datasets, but monitor the application for any slow queries or issues that might require optimization.

---

This migration plan should help you transition smoothly from SQLite to PostgreSQL while ensuring minimal disruption to your application. If you need a specific code adjustment or further details on any of the steps, let me know!
