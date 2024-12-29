from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversion
from .forms import ConversionForm

def menu_tampilan(request):
    conversions = Conversion.objects.all()  # fetch all conversions
    return render(request, 'main/menu.html', {'conversions': conversions})


def konversi_desimal(request):
    if request.method == 'POST':
        try:
            decimal = int(request.POST['number'])
            biner = bin(decimal)[2:]
            oktal = oct(decimal)[2:]
            heksadesimal = hex(decimal)[2:].upper()
            conversion = Conversion.objects.create(
                pilihan_konversi=Conversion.DECIMAL,
                decimal=decimal,
                biner=biner,
                oktal=oktal,
                heksadesimal=heksadesimal
            )
            return redirect('result', pk=conversion.pk)
        except ValueError:
            error_message = "Masukan tidak valid. Harap masukkan angka desimal."
            return render(request, 'main/desimal.html', {'error_message': error_message})
    return render(request, 'main/desimal.html')

def konversi_biner(request):
    if request.method == 'POST':
        try:
            biner = request.POST['number']
            if not all(bit in '01' for bit in biner):
                raise ValueError
            decimal = int(biner, 2)
            oktal = oct(decimal)[2:]
            heksadesimal = hex(decimal)[2:].upper()
            conversion = Conversion.objects.create(
                pilihan_konversi=Conversion.BINARY,
                decimal=decimal,
                biner=biner,
                oktal=oktal,
                heksadesimal=heksadesimal
            )
            return redirect('result', pk=conversion.pk)
        except ValueError:
            error_message = "Masukan tidak valid. Harap masukkan angka biner yang valid."
            return render(request, 'main/biner.html', {'error_message': error_message})
    return render(request, 'main/biner.html')

def konversi_oktal(request):
    if request.method == 'POST':
        try:
            oktal = request.POST['number']
            if not all(oct_digit in '01234567' for oct_digit in oktal):
                raise ValueError
            decimal = int(oktal, 8)
            biner = bin(decimal)[2:]
            heksadesimal = hex(decimal)[2:].upper()
            conversion = Conversion.objects.create(
                pilihan_konversi=Conversion.OCTAL,
                decimal=decimal,
                biner=biner,
                oktal=oktal,
                heksadesimal=heksadesimal
            )
            return redirect('result', pk=conversion.pk)
        except ValueError:
            error_message = "Masukan tidak valid. Harap masukkan angka oktal yang valid."
            return render(request, 'main/oktal.html', {'error_message': error_message})
    return render(request, 'main/oktal.html')

def konversi_heksadesimal(request):
    if request.method == 'POST':
        try:
            heksadesimal = request.POST['number']
            if not all(hex_digit in '0123456789ABCDEFabcdef' for hex_digit in heksadesimal):
                raise ValueError
            decimal = int(heksadesimal, 16)
            biner = bin(decimal)[2:]
            oktal = oct(decimal)[2:]
            conversion = Conversion.objects.create(
                pilihan_konversi=Conversion.HEXADECIMAL,
                decimal=decimal,
                biner=biner,
                oktal=oktal,
                heksadesimal=heksadesimal.upper()
            )
            return redirect('result', pk=conversion.pk)
        except ValueError:
            error_message = "Masukan tidak valid. Harap masukkan angka heksadesimal yang valid."
            return render(request, 'main/heksadesimal.html', {'error_message': error_message})
    return render(request, 'main/heksadesimal.html')

def result(request, pk):
    conversion = get_object_or_404(Conversion, pk=pk)
    return render(request, 'main/result.html', {'conversion': conversion})

def conversion_add(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if form.is_valid():
            conversion = form.save(commit=False)

            if conversion.pilihan_konversi == Conversion.DECIMAL:
                try:
                    decimal_value = int(conversion.field_name)
                    conversion.biner = bin(decimal_value)[2:]
                    conversion.oktal = oct(decimal_value)[2:]
                    conversion.heksadesimal = hex(decimal_value)[2:].upper()
                    conversion.decimal = decimal_value
                except ValueError:
                    form.add_error('field_name', 'Invalid decimal number.')

            elif conversion.pilihan_konversi == Conversion.BINARY:
                try:
                    binary_value = conversion.field_name
                    decimal_value = int(binary_value, 2)
                    conversion.decimal = decimal_value
                    conversion.oktal = oct(decimal_value)[2:]
                    conversion.heksadesimal = hex(decimal_value)[2:].upper()
                    conversion.biner = binary_value
                except ValueError:
                    form.add_error('field_name', 'Invalid binary number.')

            elif conversion.pilihan_konversi == Conversion.OCTAL:
                try:
                    octal_value = conversion.field_name
                    decimal_value = int(octal_value, 8)
                    conversion.decimal = decimal_value
                    conversion.biner = bin(decimal_value)[2:]
                    conversion.heksadesimal = hex(decimal_value)[2:].upper()
                    conversion.oktal = octal_value
                except ValueError:
                    form.add_error('field_name', 'Invalid octal number.')

            elif conversion.pilihan_konversi == Conversion.HEXADECIMAL:
                try:
                    hexadecimal_value = conversion.field_name.upper()
                    decimal_value = int(hexadecimal_value, 16)
                    conversion.decimal = decimal_value
                    conversion.biner = bin(decimal_value)[2:]
                    conversion.oktal = oct(decimal_value)[2:]
                    conversion.heksadesimal = hexadecimal_value
                except ValueError:
                    form.add_error('field_name', 'Invalid hexadecimal number.')

            if form.errors:
                return render(request, 'main/conversion_add.html', {'form': form})

            conversion.save()
            return render(request, 'main/result.html', {'conversion': conversion})

    else:
        form = ConversionForm()

    return render(request, 'main/conversion_add.html', {'form': form})

def conversion_edit(request, pk):
    conversion = get_object_or_404(Conversion, pk=pk)

    if request.method == 'POST':
        form = ConversionForm(request.POST, instance=conversion)
        if form.is_valid():
            conversion = form.save(commit=False)
            if conversion.pilihan_konversi == Conversion.DECIMAL:
                try:
                    conversion.biner = bin(int(conversion.field_name))[2:]
                    conversion.oktal = oct(int(conversion.field_name))[2:]
                    conversion.heksadesimal = hex(int(conversion.field_name))[2:].upper()
                    conversion.decimal = int(conversion.field_name)
                except ValueError:
                    form.add_error('field_name', 'Masukkan tidak valid. Harap masukkan angka desimal.')
                    return render(request, 'main/conversion_edit.html', {'form': form, 'conversion': conversion})

            elif conversion.pilihan_konversi == Conversion.BINARY:
                try:
                    conversion.decimal = int(conversion.field_name, 2)
                    conversion.oktal = oct(conversion.decimal)[2:]
                    conversion.heksadesimal = hex(conversion.decimal)[2:].upper()
                    conversion.biner = conversion.field_name
                except ValueError:
                    form.add_error('field_name', 'Masukkan tidak valid. Harap masukkan angka biner yang valid.')
                    return render(request, 'main/conversion_edit.html', {'form': form, 'conversion': conversion})

            elif conversion.pilihan_konversi == Conversion.OCTAL:
                try:
                    conversion.decimal = int(conversion.field_name, 8)
                    conversion.biner = bin(conversion.decimal)[2:]
                    conversion.heksadesimal = hex(conversion.decimal)[2:].upper()
                    conversion.oktal = conversion.field_name
                except ValueError:
                    form.add_error('field_name', 'Masukkan tidak valid. Harap masukkan angka oktal yang valid.')
                    return render(request, 'main/conversion_edit.html', {'form': form, 'conversion': conversion})

            elif conversion.pilihan_konversi == Conversion.HEXADECIMAL:
                try:
                    conversion.decimal = int(conversion.field_name, 16)
                    conversion.biner = bin(conversion.decimal)[2:]
                    conversion.oktal = oct(conversion.decimal)[2:]
                    conversion.heksadesimal = conversion.field_name.upper()
                except ValueError:
                    form.add_error('field_name', 'Masukkan tidak valid. Harap masukkan angka heksadesimal yang valid.')
                    return render(request, 'main/conversion_edit.html', {'form': form, 'conversion': conversion})

            conversion.save()
            return render(request, 'main/conversion_edit.html', {'form': form, 'conversion': conversion})
    else:
        form = ConversionForm(instance=conversion)

    return render(request, 'main/conversion_edit.html', {'form': form, 'conversion': conversion})

def conversion_delete(request, pk):
    conversion = get_object_or_404(Conversion, pk=pk)
    if request.method == 'POST':
        conversion.delete()
        return redirect('conversion_list')
    return render(request, 'main/conversion_confirm_delete.html', {'conversion': conversion})

def conversion_detail(request, pk):
    conversion = get_object_or_404(Conversion, pk=pk)
    return render(request, 'main/conversion_detail.html', {'conversion': conversion})

def conversion_list(request):
    conversions = Conversion.objects.all()
    return render(request, 'main/conversion_list.html', {'conversions': conversions})