FULLY_SPECIFIED_NAME = '900000000000003001'
if __name__ == '__main__':
    from snomed_ct.models import Concept, ICD10_Mapping, Relationship, TextDefinition, Description, ISA
    map = ICD10_Mapping.objects.filter(id='4c897844-7093-52e2-a95e-fd1334a47645')[0]
    snomed_concept = map.referenced_component
    snomed_concept = Concept.by_id(snomed_concept.id)
    print(snomed_concept)
    print(map.map_target)
    print(Description.objects.get(concept=snomed_concept,
                                  active=True,
                                  type__id=FULLY_SPECIFIED_NAME).term)
    print(TextDefinition.objects.filter(concept=snomed_concept))
    print(snomed_concept.fully_specified_name_no_type, map.map_rule, map.map_advice)
#    print(snomed_concept.expository_text())
    for rel in snomed_concept.outbound_relationships():
        print("\t- {} -> {}".format(rel.type, rel.destination))

 #   print(Concept.by_fully_specified_name(term__iregex='aort.+stenosis'))
    concept = Concept.by_id(194733006)
    print(concept)
    print(Concept.by_definition('aort.+stenosis'))
    for c in Concept.by_definition('aort.+stenosis').has_icd10_mappings():
        print(c)
        for defn in c.definitions().values_list('term', flat=True):
            print("\t", defn)
        print("\t", c.expository_text())


