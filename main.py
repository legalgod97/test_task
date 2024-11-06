def get_parent_sections(building_id: int) -> list[Section]:
  parent_sections = []
  sections = Section.objects.filter(building_id=building_id)
  for section in sections:
    if section.parent is None:
      continue
    expenditures = Expenditure.objects.filter(section=section)
    budget = sum(expenditure.count * expenditure.price for expenditure in expenditures)
    parent_sections.append({
      'section': section,
      'budget': budget
    })
  return parent_sections

def get_buildings() -> list[dict]:

  buildings = []
  for building in Building.objects.all():
    works_amount = 0
    materials_amount = 0
    for section in Section.objects.filter(building=building):
      expenditures = Expenditure.objects.filter(section=section)
      for expenditure in expenditures:
        if expenditure.type == Expenditure.Types.WORK:
          works_amount += expenditure.count * expenditure.price
        elif expenditure.type == Expenditure.Types.MATERIAL:
          materials_amount += expenditure.count * expenditure.price
    buildings.append({
      'id': building.id,
      'works_amount': works_amount,
      'materials_amount': materials_amount,
    })
  return buildings


def update_with_discount(section_id: int, discount: Decimal):
    """
    @param discount: Размер скидки в процентах от Decimal(0) до Decimal(100)
    """
    if discount < Decimal(0) or discount > Decimal(100):
        raise ValueError('Скидка должна быть от 0 до 100 процентов')

    section = Section.objects.get(pk=section_id)
    expenditures = Expenditure.objects.filter(section=section)

    for expenditure in expenditures:
        new_price = expenditure.price - (expenditure.price * discount / Decimal(100))
        expenditure.price = new_price
        expenditure.save()


