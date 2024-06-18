from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MaxValueValidator, DecimalValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CarBrand(models.Model):
    name = models.CharField( max_length=200, verbose_name="Nombre", unique=True)
    is_enable = models.BooleanField(default=True, verbose_name="Habilitado")
    class Meta:
        ordering = ['name']
        verbose_name = 'Marca'
    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_brand = models.ForeignKey(CarBrand, on_delete=models.DO_NOTHING, verbose_name="Marca")
    name = models.CharField(max_length=200, verbose_name="Nombre", unique=True)
    is_enable = models.BooleanField(default=True, verbose_name="Habilitado")
    class Meta:
        ordering = ['car_brand']
        verbose_name = 'Modelo'
    def __str__(self):
        return self.name

class CarPart(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    is_enable = models.BooleanField(default=True, verbose_name="Habilitado")
    class Meta:
        ordering = ['name']
        verbose_name = 'Item'
    def __str__(self):
        return self.name

class CarModelPart(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING, verbose_name="Modelo")
    car_part = models.ForeignKey(CarPart, on_delete=models.DO_NOTHING, null=True, verbose_name="Item")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ancho")
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Largo")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    installation_price = models.DecimalField(max_digits=10,decimal_places=2, default=0, verbose_name="Precio Instalación")
    is_enable = models.BooleanField(default=True, verbose_name="Habilitado")
    
    class Meta:
        verbose_name = 'Modelo Item'
        constraints = [
            models.UniqueConstraint(fields=['car_model', 'car_part'], name='unique_model_item'),
        ]

    def __str__(self):
        return f"{self.car_model} - {self.car_part}"
    
class WindowFilm(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description= models.TextField()
    is_enable = models.BooleanField(default=True, verbose_name="Habilitado")
    # content = HTMLField(null=True)
    class Meta:
        ordering = ['name']
        verbose_name = 'Lamina'
    def __str__(self):
        return self.name
    
class WindowFilmReel(models.Model):
    window_film = models.ForeignKey(WindowFilm,
                                       related_name="bobina_lamina",
                                       on_delete=models.DO_NOTHING, 
                                       verbose_name="Lamina")
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ancho")
    length = models.DecimalField(max_digits=10, decimal_places=2,  verbose_name="Largo")
    price = models.DecimalField(max_digits=10, decimal_places=2,  verbose_name="Precio")
    class Meta:
        ordering = ['window_film']
        verbose_name = 'Bobina'  
    
    def __str__(self):
        return f'{self.window_film.name} - {self.width}'
    

class BranchOffice(models.Model):
    name = models.CharField(max_length=20, default=" ", null=False, verbose_name="Nombre")
    address = models.CharField(max_length=400, default=" ", null=False, verbose_name="Dirección")
    enable = models.BooleanField(default=True, verbose_name="Habilitado")
    empleado = models.ManyToManyField(User, verbose_name='Empleados')
    # administrador = models.ManyToManyField(User, verbose_name='Admin Sucursal')
    def __str__(self):
        return f'{self.name}'
    

    
class Company(models.Model):
    name = models.CharField(max_length=20, default=" ", null=False, verbose_name="Nombre")
    address = models.CharField(max_length=400, default=" ", null=False, verbose_name="Dirección")
    phone_number = models.CharField(validators=[RegexValidator('(\+)*\d{7,11}')], verbose_name="Numero Telefónico", max_length=11)

    class Meta: 
        verbose_name = 'Company'
        ordering = ['name']
    def __str__(self):
        return f'{self.name}'   

class Profile(models.Model):
    name = models.CharField(max_length=400, verbose_name="Nombre")
    last_name = models.CharField(max_length=400, verbose_name="Apellido")
    phone_number = models.CharField(validators=[RegexValidator('(\+)*\d{7,11}')], verbose_name="Numero Telefónico", max_length=11)
    ci_nit = models.CharField(validators=[RegexValidator('\d*')], verbose_name="CI/NIT", max_length=20)
    type = models.CharField(choices={"syst": "System", "clie": "Client", "inst": "Instalador"}, default="client", verbose_name='Tipo Perfil', max_length=10)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Usuario', null=True)
    sucursal = models.ForeignKey(BranchOffice, on_delete=models.DO_NOTHING, blank=True, null=True)
    is_enable = models.BooleanField(default=True)
    
    class Meta: 
        verbose_name = 'Perfil'
        ordering = ['last_name', 'name']
    def __str__(self):
        return f'{self.name} {self.last_name}'    
    
class ProformaHeader(models.Model):
    created_on = models.DateTimeField(verbose_name="Fecha Proforma", auto_now=True)
    name = models.CharField(max_length=400, default=" ", null=False, verbose_name="Nombre Completo")
    email = models.CharField(validators=[EmailValidator()], null=True,verbose_name="Email", max_length=100)
    ci_nit = models.CharField(validators=[RegexValidator('\d*')],null=True, verbose_name="CI/NIT", max_length=20)
    car_plate = models.CharField(max_length=10, default="", blank=True, null=True, verbose_name="Placa Auto")
    phone_number = models.CharField(validators=[RegexValidator('(\+)*\d{7,11}')], default="", verbose_name="Numero Telefónico", max_length=11)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.DO_NOTHING,blank=True, null=True, verbose_name="Sucursal")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[DecimalValidator(max_digits=10, decimal_places=2), MinValueValidator(limit_value=0)],
                                   verbose_name="Descuento")
    discount_reason = models.TextField(verbose_name='Motivo Descuento', blank=True, null=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING, verbose_name="Modelo", blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total Pagar")
    is_delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(Profile, verbose_name='Creado Por',on_delete=models.DO_NOTHING, null=False,related_name='proforma_created_by')
    is_close = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Proforma'
        ordering = ["-id","-created_on",]

    def __str__(self) -> str:
        # prefijo = 'Proforma' if self.sales_status == self.helper.prof else 'Nota Venta'
        return f'Proforma {self.id}'
    
class Proforma_Detail(models.Model):
    proforma_header = models.ForeignKey(ProformaHeader, related_name='items', on_delete=models.DO_NOTHING, verbose_name="Proforma")
    car_part = models.ForeignKey(CarPart, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Item")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ancho" )
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Largo")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Sub Total")
    installation_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo Instalación")
    window_film_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo Lámina")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad")
    window_film = models.ForeignKey(WindowFilm, on_delete=models.DO_NOTHING, verbose_name="Lámina", null=True)
    class Meta:
        verbose_name = 'Detalle Venta'
    
    def __str__(self) -> str:
        return f'Detalle'
    
class Storage(models.Model):
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.DO_NOTHING, verbose_name="Sucursal",related_name="sucursal_inventario_in")
    reel = models.ForeignKey(WindowFilmReel, on_delete=models.DO_NOTHING, verbose_name="Bobina", related_name="bobina_inventario")
    total_length = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Longitud Inicial")
    created_on = models.DateTimeField(verbose_name="Fecha", null=False)
    numero_referencia = models.PositiveIntegerField( verbose_name="Numero Referencia",default=0, validators=[MaxValueValidator(limit_value=9999999999, message='solo se aceptan valores con 10 digitos')])
    precio_compra_mtr_lineal = models.DecimalField( max_digits=10, decimal_places=2, default=0.0, verbose_name="Precio Compra Metro Lineal")
    precio_venta_mtr_lineal = models.DecimalField( max_digits=10, decimal_places=2, default=0.0, verbose_name="Precio Venta Metro Lineal")
    def __str__(self):
        return f'{self.branch_office.name}-{self.reel.window_film.name}'

class StorageOut(models.Model):
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.DO_NOTHING, verbose_name="Sucursal",related_name="sucursal_inventario_out")
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING, verbose_name="Almacen",related_name="sucursal_inventario")
    created_on = models.DateTimeField(verbose_name="Creado en", null=False)
    length_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Metros Cortados")
    is_deleted = models.BooleanField(default=False, verbose_name="Anulado")
    deleted_on = models.DateTimeField(verbose_name="Eliminado en", null=True)


class WorkNote(models.Model):
    proforma = models.OneToOneField(ProformaHeader, on_delete=models.DO_NOTHING, blank=False, null=False, verbose_name="Proforma")
    codigo_garantia = models.CharField(null=True, blank=True, verbose_name="Codigo Garantia", max_length=12, unique=True)
    car_in_date = models.DateTimeField(verbose_name="Entrada Vehiculo", null=True, blank=True)
    car_out_date = models.DateTimeField(verbose_name="Salida Vehiculo", null=True, blank=True)
    created_on = models.DateTimeField(verbose_name="Creado en", null=False)
    notes = models.TextField(verbose_name='Observaciones', blank=True, null=True)
    # instalador = models.ForeignKey(Profile, verbose_name='Instalador',on_delete=models.DO_NOTHING, null=True, related_name='instalador_laminas_nota_trabajo')
    # responsable = models.ForeignKey(Profile, verbose_name='Responsable',on_delete=models.DO_NOTHING, blank=True, null=True, related_name='responsable_proforma_nota_trabajo')
    

    def __str__(self) -> str:
        return f'Nota Trabajo {self.id}'

    class Meta:
        verbose_name = 'Nota Trabajo'
        ordering = ["-id","-created_on"]

class WorkNoteWorker(models.Model):
    worker = models.ForeignKey(Profile, verbose_name='Trabajador',on_delete=models.DO_NOTHING, null=False)
    work_note = models.ForeignKey(WorkNote, verbose_name='Nota Trabajo',on_delete=models.DO_NOTHING, null=False)
    type = models.CharField(choices={"inst": "Instalador", "resp": "Responsable", "instalador": "Instalador"}, 
                            default="responsable", verbose_name='Tipo Trabajador', max_length = 11)
    created_on = models.DateTimeField(verbose_name="Creado en", null=False)

class WorkNoteSumary(models.Model):
    work_note = models.ForeignKey(WorkNote, on_delete=models.DO_NOTHING, verbose_name="Nota Trabajo")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ancho" )
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Largo")
    storage_out = models.ForeignKey(StorageOut, on_delete=models.DO_NOTHING, verbose_name="registro salida inventario")
    created_on = models.DateTimeField(verbose_name="Creado en", null=False)
    is_deleted = models.BooleanField(default=False, verbose_name="Anulado")
    deleted_on = models.DateTimeField(verbose_name="Eliminado en", null=True)


class PaymentNote(models.Model):
    proforma = models.ForeignKey(ProformaHeader, verbose_name='Nota Trabajo',on_delete=models.DO_NOTHING, null=False)
    payment_method =  models.CharField(choices={"bank": "Banco", "cash": "Efectivo"}, default="bank", verbose_name='Tipo Trabajador', max_length=8)
    created_on = models.DateTimeField(verbose_name="Creado en", null=False)
    created_by = models.ForeignKey(Profile, verbose_name='Creador Por',on_delete=models.DO_NOTHING, null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total Pagar")


class Account(models.Model):
    code = models.CharField(max_length=100, verbose_name="Codigo cuenta")
    name = models.CharField(max_length=400, verbose_name="Nombre")
    

class Account_Flow(models.Model):
    account = models.ForeignKey(Account, verbose_name='Cuenta',on_delete=models.DO_NOTHING, null=False)
    debe = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Debe")
    haber = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Haber")
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Saldo")
    created_on = models.DateTimeField(verbose_name="Creado en", null=False)
    created_by = models.ForeignKey(Profile, verbose_name='Creador Por',on_delete=models.DO_NOTHING, null=False)