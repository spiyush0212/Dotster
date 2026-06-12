from django.shortcuts import redirect, render

from main.models import AppForm, Application

import os 


def get_kube_config(app, user):
    kube_config = f"""apiVersion: v1
    kind: Pod
    metadata:
    name: {user.username}{app.name}
    spec:
    replicas: {app.num_replicas_min}
    template:
            metadata: 
                labels:
                    app: {user.username}{app.name}
            spec:
                containers:
                - name: {user.username}{app.name}-1
                    image: {app.docker_image_url}
                    ports:
                    - containerPort: {app.port}
    behavior:
    scaleDown:
        stabilizationWindowSeconds: 300
        policies:
        - type: Percent
        value: 100
        periodSeconds: 15
        - type: Pods
            value: {app.num_replicas_min}
            periodSeconds: 15
        selectPolicy: Max
    scaleUp:
        stabilizationWindowSeconds: 0
        policies:
        - type: Percent
        value: 100
        periodSeconds: 15
        - type: Pods
        value: {app.num_replicas_max}
        periodSeconds: 15
        selectPolicy: Max
    """
    return kube_config


def index(request):
    # check authentication  
    if not request.user.is_authenticated:
        return render(request, "login.html")

    user = request.user
    # get user's applications
    applications = user.applications.all()

    # get information from kubernetes
    status = os.system("kubectl get pods")
    
    # zip applications and app configs
    context = {
        "applications": [{ "name": app.name, "description": app.description, "current_instances": app.current_instances, "max_nodes": app.num_replicas_max, "min_nodes": app.num_replicas_min, "port": app.port, "status": "running", "url": "#", "id": app._id} for app in applications]
    } 

    print(context)
    return render(request, "index.html", context)



def create_application(request):
    # check authentication  
    if not request.user.is_authenticated:
        return render(request, "login.html")

    user = request.user

    form = AppForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            app = form.save(commit=False)
            app.owner = user
            app.current_instances = app.num_replicas_min
            app.save()

            kube_config = get_kube_config(app, user)
            
            with open("hpa.yaml", "w") as f:
                f.write(kube_config)
            os.system("kubectl apply -f hpa.yaml")
            os.system("kubectl expose deployment " + user.username + app.name + " --type=LoadBalancer --port=" + app.port)
            return redirect("/")


    context = {
        "form": form
    }

    return render(request, "create_application.html", context)


def delete_application(request, id):
    # check authentication  
    if not request.user.is_authenticated:
        return render(request, "login.html")

    user = request.user

    try:
        os.system("kubectl delete deployment " + user.username + app.name)
        app = Application.objects.get(id=id)
        app.delete()
    except:
        pass


    return redirect("/")

def rebuild_application(request, id):
    # check authentication  
    if not request.user.is_authenticated:
        return render(request, "login.html")

    user = request.user

    try:
        app = Application.objects.get(id=id)
        os.system("kubectl delete deployment " + user.username + app.name)
        kube_config = get_kube_config(app, user)
    
        with open("hpa.yaml", "w") as f:
            f.write(kube_config)
        os.system("kubectl apply -f hpa.yaml")
        os.system("kubectl expose deployment " + user.username + app.name + " --type=LoadBalancer --port=" + app.port)
    except:
        pass

    return redirect("/")

def update_application(request, id):
    # check authentication  
    if not request.user.is_authenticated:
        return render(request, "login.html")

    user = request.user

    try:
        app = Application.objects.get(id=id)
        form = AppForm(request.POST or None, instance=app)
        if request.method == "POST":
            if form.is_valid():
                app = form.save(commit=False)
                app.owner = user
                app.save()
                os.system("kubectl delete deployment " + user.username + app.name)
                kube_config = get_kube_config(app, user)
            
                with open("hpa.yaml", "w") as f:
                    f.write(kube_config)
                os.system("kubectl apply -f hpa.yaml")
                os.system("kubectl expose deployment " + user.username + app.name + " --type=LoadBalancer --port=" + app.port)
                return redirect("/")
    except:
        pass

    context = {
        "form": form
    }

    return render(request, "create_application.html", context)


def clone_application(request, id):
    # check authentication  
    if not request.user.is_authenticated:
        return render(request, "login.html")

    user = request.user

    try:
        app = Application.objects.get(id=id)
        form = AppForm(request.POST or None, instance=app)
        if request.method == "POST":
            if form.is_valid():
                app = form.save(commit=False)
                app.owner = user
                app.save()
                kube_config = get_kube_config(app, user)
            
                with open("hpa.yaml", "w") as f:
                    f.write(kube_config)
                os.system("kubectl apply -f hpa.yaml")
                os.system("kubectl expose deployment " + user.username + app.name + " --type=LoadBalancer --port=" + app.port)
                return redirect("/")
    except:
        pass

    context = {
        "form": form
    }

    return render(request, "create_application.html", context)