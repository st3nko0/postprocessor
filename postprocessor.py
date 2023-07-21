import os
import pandas as pd

# Относительный путь к таблицам Excel
square_profile = os.path.join('database', 'Гнутые замкнутые сварные квадратные профили по ГОСТ 30245-2003.xlsx')
rectangular_profile = os.path.join('database', 'Гнутые замкнутые сварные прямоугольные профили по ГОСТ 30245-2003.xlsx')

# Преобразуем таблицы Excel в DataFrame Pandas
df_square = pd.read_excel(square_profile)
df_rectangular = pd.read_excel(rectangular_profile)

# Преобразуем DataFrame 'square' к виду DataFrame 'rectangular'
df_square['h, мм'] = df_square['b, мм'].copy()
df_square['Iy, см4'] = df_square['Iy=Iz, см4'].copy()
df_square['Wy, см3'] = df_square['Wy=Wz, см3'].copy()
df_square['iy, мм'] = df_square['iy=iz, мм'].copy()
df_square['Iz, см4'] = df_square['Iy=Iz, см4'].copy()
df_square['Wz, см3'] = df_square['Wy=Wz, см3'].copy()
df_square['iz, мм'] = df_square['iy=iz, мм'].copy()

# Удалим ненужные столбцы из DataFrame 'square'
df_square = df_square.drop(['Iy=Iz, см4', 'Wy=Wz, см3', 'iy=iz, мм'], axis=1)

# Объединим DataFrame 'square' и DataFrame 'rectangular'
df_profiles = pd.concat([df_rectangular, df_square], axis=0, ignore_index=True)

class Element():
    def __init__(self, depth, width, thickness, radius, area,
                 yMomentInertia, yMomentResistance, yRadiusGyration,
                 zMomentInertia, zMomentResistance, zRadiusGyration,
                 MassPerUnitLength):
        self.h = depth
        self.b = width
        self.s = thickness
        self.R = radius
        self.A = area
        self.Iy = yMomentInertia
        self.Wy = yMomentResistance
        self.iy = yRadiusGyration
        self.Iz = zMomentInertia
        self.Wz = zMomentResistance
        self.iz = zRadiusGyration
        self.P = MassPerUnitLength


class TrussMember:
    def __init__(self, length, force, selected_section, area, moment_of_inertia):
        self.length = length
        self.force = force
        self.selected_section = selected_section
        self.area = area
        self.moment_of_inertia = moment_of_inertia
        self.utilization_factor = None

    def calculate_utilization_factor(self):
        # Предположим некоторую приложенную нагрузку и свойства материала (замените на фактические значения)
        applied_load = 1000.0  # Пример: Приложенная нагрузка в Н (ньютонах) или кН (килоньютонах)
        yield_strength = 300.0  # Пример: Предел прочности материала в МПа

        # Рассчитать аксиальное напряжение в элементе.
        axial_stress = abs(self.force) / self.area

        # Рассчитайте коэффициент использования.
        self.utilization_factor = axial_stress / (yield_strength / 1e6)  # Переведите МПа в Н/мм^2

def calculate_utilization_factors(df_sections):
    for index, row in df_sections.iterrows():
        member = TrussMember(
            length=row['Length'],
            force=row['Force'],
            selected_section=row['Selected Section'],
            area=row['Area'],
            moment_of_inertia=row['Moment of Inertia']
        )
        member.calculate_utilization_factor()
        df_sections.at[index, 'Utilization Factor'] = member.utilization_factor

# Пример DataFrame (замените на свой фактический DataFrame)
data = {
    'Length': [10.0, 15.0],
    'Force': [-100.0, 150.0],
    'Selected Section': ["Section A", "Section B"],
    'Area': [100.0, 200.0],
    'Moment of Inertia': [5000.0, 8000.0],
}

df_sections = pd.DataFrame(data)

# Рассчитайте коэффициенты использования и обновите DataFrame
calculate_utilization_factors(df_sections)

print(df_sections)


"""НЕ очень удачная версия кода по проверке сечения"""
class TrussMember:
    def __init__(self, length, force, selected_section, area, moment_of_inertia):
        self.length = length
        self.force = force
        self.selected_section = selected_section
        self.area = area
        self.moment_of_inertia = moment_of_inertia
        self.utilization_factor = None

    def calculate_utilization_factor(self):
        # Предположим некоторую приложенную нагрузку и свойства материала (замените на фактические значения)
        applied_load = 1000.0  # Пример: Приложенная нагрузка в Н (ньютонах) или кН (килоньютонах)
        yield_strength = 300.0  # Пример: Предел прочности материала в МПа

        # Рассчитать аксиальное напряжение в элементе.
        axial_stress = abs(self.force) / self.area

        # Рассчитайте коэффициент использования.
        self.utilization_factor = axial_stress / (yield_strength / 1e6)  # Конвертировать МПа в Н/мм^2

def calculate_utilization_factors(truss_members):
    for member in truss_members:
        member.calculate_utilization_factor()

def create_dataframe(truss_members):
    data = [member.__dict__ for member in truss_members]
    df_sections = pd.DataFrame(data)
    return df_sections

# Пример использования
truss_members = [
    TrussMember(length=10.0, force=-100.0, selected_section="Section A", area=100.0, moment_of_inertia=5000.0),
    TrussMember(length=15.0, force=150.0, selected_section="Section B", area=200.0, moment_of_inertia=8000.0),
    # Добавьте больше элементов по мере необходимости
]

calculate_utilization_factors(truss_members)
selected_sections_df = create_dataframe(truss_members)
print(selected_sections_df)



"""Код из ChatGPT для подбора поперчного сечения"""
class TrussMember:
    def __init__(self, length, force):
        self.length = length
        self.force = force
        self.selected_section = None
        self.area = None
        self.moment_of_inertia = None

    def select_section(self):
        # Рассчитать требуемые сечения на основе силы и длины.
        # (Вам понадобятся фактические расчеты дизайна здесь)
        self.moment_of_inertia = ...
        self.area = ...

        # Выберите подходящий стальной профиль из AISC на основе требуемых характеристик.
        # (Вам понадобится актуальная ссылка на код AISC и поиск здесь)
        self.selected_section = ...

    def to_dict(self):
        return {
            'Length': self.length,
            'Force': self.force,
            'Selected Section': self.selected_section,
            'Area': self.area,
            'Moment of Inertia': self.moment_of_inertia
        }

def select_steel_sections(truss_members):
    data = [member.to_dict() for member in truss_members]
    df_sections = pd.DataFrame(data)
    return df_sections

# Пример использования
truss_members = [
    TrussMember(length=10.0, force=-100.0),  # Пример сжатого элемента
    TrussMember(length=15.0, force=150.0),   # Пример растянутого элемента
    # Добавьте больше элементов по мере необходимости.
]

selected_sections_df = select_steel_sections(truss_members)
print(selected_sections_df)
