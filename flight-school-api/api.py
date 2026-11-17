import flask
import logging

import pandas as pd
import psycopg2
import datetime
import pandas as pd

app = flask.Flask(__name__)

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

config = pd.read_json('config.json', typ='series')

def db_connection():

    db = psycopg2.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
        database=config['database']
    )

    return db




@app.route('/') 
def landing_page():
    return '''
        REST API Landing Page <br/><br/>
        Check the sources for instructions on how to use the endpoints<br/><br/>
        SGD 2022<br/><br/>
    '''

@app.route('/proj/pilot/<pilot_id>', methods=['PUT'])
def update_pilot(pilot_id):
    logger.info('PUT /proj/pilot/<pilot_id>')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'PUT /proj/pilot/<pilot_id> - payload: {payload}')

    try:
        if 'first_name' in payload:
            statment = 'UPDATE pilot SET first_name = %s WHERE id = %s'
            values = (payload['first_name'],pilot_id)
            cur.execute(statment,values)
        if 'last_name' in payload:
            statment = 'UPDATE pilot SET last_name = %s WHERE id = %s'
            values = (payload['last_name'],pilot_id)
            cur.execute(statment,values)
        if 'address' in payload:
            statment = 'UPDATE pilot SET address = %s WHERE id = %s'
            values = (payload['address'],pilot_id)
            cur.execute(statment,values)
        if 'home_airport' in payload:
            statment = 'UPDATE pilot SET home_airport = %s WHERE id = %s'
            values = (payload['home_airport'],pilot_id)
            cur.execute(statment,values)
        if 'license' in payload:
            if 'end_date' in payload:
                statment = 'INSERT INTO Flight_license(license,end_date,pilot_id) Values (%s,%s,%s)'
                values = (payload['license'],payload['license_validity'],pilot_id)
                cur.execute(statment, values)
        if 'medical_validity' in payload:
            if 'end_date' in payload:
                statment = 'INSERT INTO Medical_certificate(end_date,pilot_id) Values (%s,%s)'
                values = (payload['license'], pilot_id)
                cur.execute(statment, values)

        response = {'status': StatusCodes['success']}
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/pilot/<keyword>', methods=['GET'])
def search_pilot(keyword):
    logger.info('GET /proj/pilot/<keyword>')

    logger.debug(f'keyword : {keyword}')

    conn = db_connection()
    cur = conn.cursor()
    try:
        keyword = '%' + keyword + '%'
        cur.execute('SELECT id,first_name,last_name,address,home_airport FROM pilot where lower(first_name) like lower(%s) or lower(last_name) like lower(%s) or lower(address) like lower(%s) or lower(home_airport) like lower(%s)', (keyword,keyword,keyword,keyword,))
        rows = cur.fetchall()

        content = []

        logger.debug('GET /proj/pilot/<keyword> - parse')
        logger.debug(rows)
        for row in rows:
            content.append( {'pilot_id': row[0], 'first_name': row[1], 'last_name': row[2],'address':row[3],'home_airport':row[4]})
        response = {'status': StatusCodes['success'], 'results': content}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /proj/pilot/<keyword> - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/pilot/<int:pilot_id>', methods=['GET'])
def consult_details_pilot(pilot_id):
    logger.info('GET /proj/pilot/<pilot_id>')

    logger.debug(f'pilot_id : {pilot_id}')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT id,first_name,last_name,address,home_airport,aircraft_type_type as aircraft_type,start_date,end_date,book_start,book_end,booking_type_id as booking_type,airport_airport_code,airport_airport_code1,flight_start,flight_end,landings,passengers from pilot natural left join aircraft_ratings natural left join booking natural left join logbook where id = %s', (pilot_id,))
        rows = cur.fetchall()

        row = rows[0]

        logger.debug('GET /proj/pilot/<pilot_id> - parse')
        logger.debug(row)
        content = {'pilot':[{'pilot_id': row[0], 'first_name': row[1], 'last_name': row[2], 'address': row[3], 'home_airport': row[4]}],
     'aircraft_ratings':[{'aircraft_type': row[5], 'rating_start': row[6], 'rating_end': row[7]}],
     'booking':[{'book_start': row[8], 'book_end': row[9], 'booking_type': row[10]}],
     'logs':[{'flight_from': row[11], 'flight_to': row[12], 'flight_start': row[13], 'flight_end': row[14],
            'landings': row[15], 'passengers': row[16]}]
     }

        response = {'status': StatusCodes['success'], 'results': content}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /proj/pilot/<pilot_id - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/aircraft', methods=['POST'])
def add_aircraft_details():
    logger.info('POST /proj/aircraft/')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    if 'tail_number' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'tail_number value not in payload'}
        return flask.jsonify(response),response['status']
    if 'serial_number' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'serial_number value not in payload'}
        return flask.jsonify(response),response['status']
    if 'category' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'category value not in payload'}
        return flask.jsonify(response), response['status']
    if 'home_airport' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'home_airport value not in payload'}
        return flask.jsonify(response),response['status']
    if 'color' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'color value not in payload'}
        return flask.jsonify(response),response['status']

    statement = 'INSERT INTO aircraft (tail_number, serial_number, color, airport_airport_code, aircraft_type_type) VALUES (%s,%s,%s,%s,%s) RETURNING aircraft_id'
    values = (payload['tail_number'], payload['serial_number'], payload['color'], payload['home_airport'], payload['category'],)

    try:
        # verificar se serial_number já existe
        cur.execute('SELECT aircraft_id from aircraft WHERE serial_number = %s', (payload['serial_number'],))
        row = cur.fetchone()

        if row is not None:
            response = {'status': StatusCodes['api_error'], 'errors': "serial_number already registered"}
            return flask.jsonify(response), response['status']

        # verificar se tail_number já existe
        cur.execute('SELECT aircraft_id from aircraft WHERE tail_number = %s', (payload['tail_number'],))
        row = cur.fetchone()

        if row is not None:
            response = {'status': StatusCodes['api_error'], 'errors': "tail_number already registered"}
            return flask.jsonify(response), response['status']

        # insertion
        cur.execute(statement, values)

        row = cur.fetchone()[0]

        # commit the transaction
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'{row}'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /proj/aircraft - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/booking', methods=['POST'])
def register_booking():
    logger.info('POST /proj/booking/')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /proj/booking - payload: {payload}')

    if 'aircraft_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'aircraft_id value not in payload'}
        return flask.jsonify(response),response['status']
    if 'booking_type' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'booking_type value not in payload'}
        return flask.jsonify(response),response['status']
    if 'booking_start' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'booking_start value not in payload'}
        return flask.jsonify(response),response['status']
    if 'booking_end' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'booking_end value not in payload'}
        return flask.jsonify(response),response['status']
    if 'pilot_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'pilot_id value not in payload'}
        return flask.jsonify(response),response['status']
    payload['booking_start'] = datetime.datetime.strptime(payload['booking_start'], "%d-%m-%Y %H:%M")
    payload['booking_end'] = datetime.datetime.strptime(payload['booking_end'], "%d-%m-%Y %H:%M")

    statement = 'SELECT pilot_type_id, flight_license.end_date, medical_certificate.end_date from pilot join flight_license on pilot.id= flight_license.pilot_id join medical_certificate on pilot.id = medical_certificate.pilot_id WHERE pilot.id=%s '
    values = (payload['pilot_id'],)

    try:
        cur.execute(statement, values)
        rows = cur.fetchall()
        logger.debug(rows)
        if rows[0][0] == 1:
            response = {'status': StatusCodes['api_error'], 'errors': "Students can't book"}
            return flask.jsonify(response),response['status']
        if len(rows) == 0 or rows[0][1] is None:
            response = {'status': StatusCodes['api_error'], 'errors': "Pilot does not exist or no license atributed"}
            return flask.jsonify(response), response['status']

        # validades
        x = 0
        for line in rows:
            if line[1] > payload['booking_end']:
                x = 1
        if x == 0:
            response = {'status': StatusCodes['api_error'], 'errors': "License expired"}
            return flask.jsonify(response), response['status']

        x = 0
        for line in rows:
            if line[2] > payload['booking_end']:
                x = 1
        if x == 0:
            response = {'status': StatusCodes['api_error'], 'errors': "Medical certificate expired"}
            return flask.jsonify(response), response['status']

        # verificar se aeronave já está marcada

        cur.execute('SELECT id from booking WHERE aircraft_aircraft_id = %s and book_start >= %s and book_start <= %s',(payload['aircraft_id'], payload['booking_start'], payload['booking_end']))
        row = cur.fetchone()

        if row is not None:
            response = {'status': StatusCodes['api_error'], 'errors': "Aircraft already booked for this date"}
            return flask.jsonify(response), response['status']

        # verificar se piloto já tem alguma marcação para o mesmo tempo

        cur.execute('SELECT id from booking WHERE pilot_id = %s and book_start >= %s and book_start <= %s',(payload['pilot_id'], payload['booking_start'], payload['booking_end']))
        row = cur.fetchone()

        if row is not None:
            response = {'status': StatusCodes['api_error'], 'errors': "Pilot has another booking at this date"}
            return flask.jsonify(response), response['status']

        # inserção
        cur.execute('INSERT INTO BOOKING(book_start,book_end,booking_type_id,aircraft_aircraft_id,pilot_id) VALUES(%s,%s,%s,%s,%s) returning id',(payload['booking_start'],payload['booking_end'],payload['booking_type'],payload['aircraft_id'],payload['pilot_id']))
        row = cur.fetchone()[0]
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'{row}'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /proj/booking - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/booking/<int:day>-<int:month>-<int:year>', methods=['GET'], strict_slashes=True)
def list_all_bookings_specific_date(day,month,year):
    logger.info('GET /proj/booking/<day>-<month>-<year>')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT booking.id,aircraft_id,tail_number,pilot_id,first_name ,last_name ,booking_type_id,book_start,book_end FROM booking left join pilot on pilot.id = booking.pilot_id left join aircraft on aircraft.aircraft_id = booking.aircraft_aircraft_id WHERE EXTRACT(YEAR from book_start) = %s and EXTRACT(MONTH from book_start) = %s and EXTRACT(DAY from book_start) = %s',(int(year),int(month),int(day),))
        rows = cur.fetchall()

        logger.debug('GET /proj/booking/<day>-<month>-<year> - parse')
        Results = []
        for row in rows:
            logger.debug(row)
            content = {'booking_id': row[0], 'aircraft_id': row[1], 'tail_number': row[2],'pilot_id':row[3],'first_name':row[4],'last_name':row[5],'booking_type':row[6],'booking_start':row[7],'booking':row[8]}
            Results.append(content)  # appending to the payload to be returned

        response = {'status': StatusCodes['success'], 'results': Results}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET proj/booking/<year>-<month>-<day> - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/report/year_booking/<int:year>', methods=['GET'])
def ten_pilots_most_bookings(year):
    logger.info('GET /proj/report/year_booking/<year>')

    logger.debug(f'year : {year}')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT pilot_id,pilot.first_name,pilot.last_name,book_start,book_end - book_start as booked_hours FROM booking left join pilot on pilot.id = booking.pilot_id where EXTRACT(YEAR FROM booking.book_start) = %s', (year,))
        rows = cur.fetchall()

        info = []
        for i in range(len(rows)):
            row = rows[i]
            logger.debug(row)
            horas = rows[i][4]
            verificar = 0
            for j in range(len(info)):
                if row[0] == info[j][0]:
                    info[j][4] += rows[i][4]   # adicionar horas
                    info[j][3] += 1            # adicionar reservas
                    verificar = 1
            if verificar == 0:
                info.append([row[0], row[1], row[2], 1, horas])
        info.sort(reverse=True, key=lambda x: x[3])

        info = info[:10]
        logger.debug(info)

        logger.debug('GET /proj/report/year_booking/<year> - parse')

        content = [{'pilot_id': pilot[0], 'first_name': pilot[1], 'last_name': pilot[2], 'booking_count': pilot[3], 'booked_hours': str(pilot[4])} for pilot in info]

        response = {'status': StatusCodes['success'], 'results': content}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /proj/report/year_booking/<year> - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

@app.route('/proj/report/monthly_booking/<aircraft_id>', methods=['GET'])
def last_30_days(aircraft_id):
    logger.info('GET /report/monthly_booking/<aircraft_id>')

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT aircraft_aircraft_id, book_end - book_start as book_hours, book_start FROM booking where aircraft_aircraft_id =%s',(aircraft_id,))
        rows = cur.fetchall()
        logger.debug(rows)

        info = [[day, 0, datetime.timedelta(0)] for day in (delta(datetime.datetime.now() - datetime.timedelta(30), datetime.datetime.now()))]

        for day in info:
            for i in range(len(rows)):
                if rows[i][2].day == day[0].day:
                    day[1] += 1
                    day[2] += rows[i][1]

        content = [{"date": day[0], "total_bookings": day[1], "book_hours": str(day[2])} for day in info]
        response = {'status': StatusCodes['success'], 'results': content}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /report/monthly_booking/<aircraft_id> - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']


def delta(start, end):
    while start < end:
        yield start
        start += datetime.timedelta(days=1)


@app.route('/proj/flightlog', methods=['POST'])
def register_flightlog():
    logger.info('POST /proj/flightlog')
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /proj/flightlog - payload: {payload}')

    if 'pilot_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'pilot_id value not in payload'}
        return flask.jsonify(response),response['status']
    if 'aircraft_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'aircraft_id value not in payload'}
        return flask.jsonify(response),response['status']
    if 'flight_start' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'flight_start value not in payload'}
        return flask.jsonify(response),response['status']
    if 'flight_end' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'flight_end value not in payload'}
        return flask.jsonify(response),response['status']
    if 'flight_from' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'flight_from value not in payload'}
        return flask.jsonify(response),response['status']
    if 'flight_to' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'flight_to value not in payload'}
        return flask.jsonify(response),response['status']
    if 'landings' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'landings value not in payload'}
        return flask.jsonify(response),response['status']
    if 'passengers' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'passengers value not in payload'}
        return flask.jsonify(response),response['status']

    it = datetime.datetime.strptime(payload['flight_start'], "%d-%m-%Y %H:%M")
    ft = datetime.datetime.strptime(payload['flight_end'], "%d-%m-%Y %H:%M")

    i1 = it - datetime.timedelta(hours=1)
    i2 = it + datetime.timedelta(hours=1)
    f1 = ft - datetime.timedelta(hours=1)
    f2 = ft + datetime.timedelta(hours=1)

    statement = 'SELECT id from booking WHERE aircraft_aircraft_id = %s and book_start >= %s and book_start <= %s and book_end >= %s and book_end <= %s'
    values = (payload['aircraft_id'], i1, i2, f1, f2)

    try:
        cur.execute(statement,values)
        row = cur.fetchone()

        if row is None:
            response = {'status': StatusCodes['api_error'], 'results': "Booking_id doesn't exist"}
            return flask.jsonify(response),response['status']

        booking_id = row[0]

        statement = 'INSERT INTO logbook(flight_start,flight_end,landings,passengers,airport_airport_code, airport_airport_code1,booking_id) VALUES (%s,%s,%s,%s,%s,%s,%s) returning id'
        values = (it, ft,payload['landings'], payload['passengers'],payload['flight_from'], payload['flight_to'],booking_id)
        cur.execute(statement, values)

        row = cur.fetchone()[0]

        dic = {"booking_id": booking_id, "log_entry_id": row}
        # commit the transaction
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': dic}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /proj/flightlog - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'results': str(error)}

        # an error occurred, rollback
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response),response['status']

if __name__ == '__main__':
    # set up logging
    logging.basicConfig(filename='log_file.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')
    #http://127.0.0.1:8080
    #PUT http://localhost:8080/proj/pilot/<12345>
    #http://localhost:8080/proj/aircraft -H 'Content-Type: application/json' -d '{"12345": "N-UJNGD", "112321465": "Helicopter", "blue": }
    #aircraft_id, tail_number,serial_number,category,color
    #http://127.0.0.1:8080/proj/aircraft/get
    #curl -X POST http://127.0.0.1:5432/proj/aircraft/ -H 'Content-Type: application/json' -d '{"aircraft_id": "12345", "tail_number": "N-JSAFSF", "serial_number": "132456756", "caregory": "Helicopter", "color": "Blue"}'
    #http://127.0.0.1:8080/proj/pilot/12354