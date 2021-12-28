from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse
from .models import Order, OrderItem

# Register your models here.


def export_to_csv(modeladmin, queryset):
    table_meta = modeladmin.model._meta
    content_disposition = "attachment; filename={table_meta.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = get_fields(table_meta)
    writer = write_fields(writer, fields)
    set_values(writer, fields, queryset)
    return response


def get_fields(table_meta):
    fields = [
        field
        for field in table_meta.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    return fields


def write_fields(writer, fields):
    writer.writerow([field.verbose_name for field in fields])
    return writer


def set_values(writer, fields, queryset):
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
