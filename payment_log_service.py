import random
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

def generate_payment_log_entry():
    services = ["payment-gateway", "payment-processor", "fraud-detection", "account-service"]
    levels = ["INFO", "WARN", "ERROR"]
    currencies = ["USD", "EUR", "GBP", "JPY"]

    timestamp = datetime.utcnow() - timedelta(minutes=random.randint(0, 60))
    level = random.choices(levels, weights=[0.7, 0.2, 0.1])[0]
    service = random.choice(services)
    transaction_id = f"tx-{uuid.uuid4().hex[:8]}"
    customer_id = f"cust-{random.randint(100, 999)}"

    log_entry = {
        "timestamp": timestamp.isoformat() + "Z",
        "level": level,
        "service": service,
        "transactionId": transaction_id,
        "customerId": customer_id
    }

    if service == "payment-gateway":
        if level == "INFO":
            log_entry["message"] = random.choice([
                "Payment transaction initiated",
                "Payment transaction completed successfully"
            ])
            log_entry["amount"] = round(random.uniform(10, 1000), 2)
            log_entry["currency"] = random.choice(currencies)
        elif level == "ERROR":
            log_entry["message"] = "Payment transaction failed"
            log_entry["error"] = random.choice([
                "Insufficient funds",
                "Card expired",
                "Invalid card number"
            ])
    elif service == "payment-processor":
        log_entry["message"] = "Processing payment"
        log_entry["processorId"] = f"proc-{random.randint(100, 999)}"
    elif service == "fraud-detection":
        log_entry["message"] = "Suspicious activity detected"
        log_entry["risk_score"] = round(random.uniform(0.5, 1), 2)
    elif service == "account-service":
        log_entry["message"] = random.choice([
            "Account balance updated",
            "New account created",
            "Account details modified"
        ])

    return log_entry

def generate_pcf_event():
    event_types = [
        "APP_START", "CONTAINER_METRIC", "APP_LOG", "HEALTH_CHECK", "SCALING",
        "APP_CRASH", "APP_UPDATE", "ROUTE_UPDATE", "SERVICE_BINDING", "AUDIT"
    ]
    container_ids = [f"{uuid.uuid4().hex[:12]}" for _ in range(10)]
    timestamp = datetime.utcnow() - timedelta(minutes=random.randint(0, 60))
    event_type = random.choice(event_types)
    instance_index = random.randint(0, 9)

    event = {
        "timestamp": timestamp.isoformat() + "Z",
        "event_type": event_type,
        "app_name": "china-bank",
        "instance_index": instance_index,
        "container_id": container_ids[instance_index]
    }

    if event_type == "APP_START":
        event["message"] = "Application started successfully"
    elif event_type == "CONTAINER_METRIC":
        event["cpu_percentage"] = random.randint(1, 100)
        event["memory_bytes"] = random.randint(100000000, 1000000000)
        event["disk_bytes"] = random.randint(500000000, 2000000000)
    elif event_type == "APP_LOG":
        event["message"] = f"Processing transaction for customer ID: {random.randint(10000, 99999)}"
    elif event_type == "HEALTH_CHECK":
        event["status"] = random.choice(["PASSED", "FAILED"])
        event["details"] = "All endpoints responding within threshold" if event["status"] == "PASSED" else "Database connection timeout"
    elif event_type == "SCALING":
        prev_count = random.randint(5, 15)
        event["instance_count"] = {
            "previous": prev_count,
            "current": prev_count + random.choice([-2, -1, 1, 2])
        }
        event["reason"] = "Increased load detected" if event["instance_count"]["current"] > prev_count else "Decreased load detected"
    elif event_type == "APP_CRASH":
        event["reason"] = random.choice(["Out of memory", "Unhandled exception", "Deadlock detected"])
        event["exit_description"] = f"Container terminated due to {event['reason']}"
    elif event_type == "APP_UPDATE":
        event["changes"] = {
            "instances": random.randint(5, 15),
            "memory": random.choice([512, 1024, 2048]),
            "disk_quota": random.choice([1024, 2048, 4096])
        }
        event["user"] = f"{random.choice(['admin', 'developer', 'ops'])}@chinabank.com"
    elif event_type == "ROUTE_UPDATE":
        event["route"] = f"api.chinabank.com/v{random.randint(1, 3)}"
        event["action"] = random.choice(["MAP", "UNMAP"])
    elif event_type == "SERVICE_BINDING":
        event["service_instance"] = random.choice(["mysql-db", "redis-cache", "elasticsearch"])
        event["action"] = random.choice(["BIND", "UNBIND"])
    elif event_type == "AUDIT":
        event["user"] = f"{random.choice(['security', 'admin', 'system'])}@chinabank.com"
        event["action"] = random.choice(["PASSWORD_CHANGE", "ROLE_UPDATE", "ACCESS_GRANTED"])
        event["status"] = random.choice(["SUCCESS", "FAILURE"])

    return event

@app.route('/generate-logs', methods=['GET'])
def generate_logs():
    count = request.args.get('count', default=100, type=int)
    log_type = request.args.get('type', default='payment', type=str)

    if log_type == 'payment':
        logs = [generate_payment_log_entry() for _ in range(count)]
    elif log_type == 'pcf':
        logs = [generate_pcf_event() for _ in range(count)]
    else:
        return jsonify({"error": "Invalid log type. Use 'payment' or 'pcf'."}), 400

    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
