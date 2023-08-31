#include "element_factory.h"

#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/serialization/shared_ptr.hpp>

#include "elements/booleans/empty.h"
#include "elements/booleans/inclusion.h"
#include "elements/booleans/nullary.h"
#include "elements/concepts/all.h"
#include "elements/concepts/bot.h"
#include "elements/concepts/and.h"
#include "elements/concepts/diff.h"
#include "elements/concepts/equal.h"
#include "elements/concepts/not.h"
#include "elements/concepts/one_of.h"
#include "elements/concepts/or.h"
#include "elements/concepts/projection.h"
#include "elements/concepts/primitive.h"
#include "elements/concepts/some.h"
#include "elements/concepts/subset.h"
#include "elements/concepts/top.h"
#include "elements/numericals/concept_distance.h"
#include "elements/numericals/count.h"
#include "elements/numericals/role_distance.h"
#include "elements/numericals/sum_concept_distance.h"
#include "elements/numericals/sum_role_distance.h"
#include "elements/roles/and.h"
#include "elements/roles/compose.h"
#include "elements/roles/diff.h"
#include "elements/roles/identity.h"
#include "elements/roles/inverse.h"
#include "elements/roles/not.h"
#include "elements/roles/or.h"
#include "elements/roles/primitive.h"
#include "elements/roles/restrict.h"
#include "elements/roles/top.h"
#include "elements/roles/transitive_closure.h"
#include "elements/roles/transitive_reflexive_closure.h"
#include "parser/parser.h"
#include "parser/expressions/expression.h"


namespace dlplan::core {
SyntacticElementFactoryImpl::SyntacticElementFactoryImpl()
    : m_vocabulary_info(nullptr), m_caches(Caches()) {
}

SyntacticElementFactoryImpl::SyntacticElementFactoryImpl(std::shared_ptr<VocabularyInfo> vocabulary_info)
    : m_vocabulary_info(vocabulary_info), m_caches(Caches()) {
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::parse_concept(SyntacticElementFactory& parent, const std::string &description) {
    auto concept = parser::Parser().parse(description)->parse_concept(parent);
    if (!concept) {
        throw std::runtime_error("SyntacticElementFactoryImpl::parse_concept - Unable to parse concept.");
    }
    return concept;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::parse_role(SyntacticElementFactory& parent, const std::string &description) {
    auto role = parser::Parser().parse(description)->parse_role(parent);
    if (!role) {
        throw std::runtime_error("SyntacticElementFactoryImpl::parse_role - Unable to parse role.");
    }
    return role;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::parse_numerical(SyntacticElementFactory& parent, const std::string &description) {
    auto numerical = parser::Parser().parse(description)->parse_numerical(parent);
    if (!numerical) {
        throw std::runtime_error("SyntacticElementFactoryImpl::parse_numerical - Unable to parse numerical.");
    }
    return numerical;
}

std::shared_ptr<const Boolean> SyntacticElementFactoryImpl::parse_boolean(SyntacticElementFactory& parent, const std::string &description) {
    auto boolean = parser::Parser().parse(description)->parse_boolean(parent);
    if (!boolean) {
        throw std::runtime_error("SyntacticElementFactoryImpl::parse_boolean - Unable to parse boolean.");
    }
    return boolean;
}

std::shared_ptr<const Boolean> SyntacticElementFactoryImpl::make_empty_boolean(const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_boolean_cache->insert(std::make_unique<EmptyBoolean<Concept>>(m_vocabulary_info, m_caches.m_boolean_cache->size(), concept)).first;
}

std::shared_ptr<const Boolean> SyntacticElementFactoryImpl::make_empty_boolean(const std::shared_ptr<const Role>& role) {
    return m_caches.m_boolean_cache->insert(std::make_unique<EmptyBoolean<Role>>(m_vocabulary_info, m_caches.m_boolean_cache->size(), role)).first;
}

std::shared_ptr<const Boolean> SyntacticElementFactoryImpl::make_inclusion_boolean(const std::shared_ptr<const Concept>& concept_left, const std::shared_ptr<const Concept>& concept_right) {
    return m_caches.m_boolean_cache->insert(std::make_unique<InclusionBoolean<Concept>>(m_vocabulary_info, m_caches.m_boolean_cache->size(), concept_left, concept_right)).first;
}

std::shared_ptr<const Boolean> SyntacticElementFactoryImpl::make_inclusion_boolean(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_boolean_cache->insert(std::make_unique<InclusionBoolean<Role>>(m_vocabulary_info, m_caches.m_boolean_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Boolean> SyntacticElementFactoryImpl::make_nullary_boolean(const Predicate& predicate) {
    return m_caches.m_boolean_cache->insert(std::make_unique<NullaryBoolean>(m_vocabulary_info, m_caches.m_boolean_cache->size(), predicate)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_all_concept(const std::shared_ptr<const Role>& role, const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_concept_cache->insert(std::make_unique<AllConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), role, concept)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_and_concept(const std::shared_ptr<const Concept>& concept_left, const std::shared_ptr<const Concept>& concept_right) {
    return m_caches.m_concept_cache->insert(std::make_unique<AndConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), concept_left, concept_right)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_bot_concept() {
    return m_caches.m_concept_cache->insert(std::make_unique<BotConcept>(m_vocabulary_info, m_caches.m_concept_cache->size())).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_diff_concept(const std::shared_ptr<const Concept>& concept_left, const std::shared_ptr<const Concept>& concept_right) {
    return m_caches.m_concept_cache->insert(std::make_unique<DiffConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), concept_left, concept_right)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_equal_concept(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_concept_cache->insert(std::make_unique<EqualConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_not_concept(const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_concept_cache->insert(std::make_unique<NotConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), concept)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_one_of_concept(const Constant& constant) {
    return m_caches.m_concept_cache->insert(std::make_unique<OneOfConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), constant)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_or_concept(const std::shared_ptr<const Concept>& concept_left, const std::shared_ptr<const Concept>& concept_right) {
    return m_caches.m_concept_cache->insert(std::make_unique<OrConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), concept_left, concept_right)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_projection_concept(const std::shared_ptr<const Role>& role, int pos) {
    return m_caches.m_concept_cache->insert(std::make_unique<ProjectionConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), role, pos)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_primitive_concept(const Predicate& predicate, int pos) {
    return m_caches.m_concept_cache->insert(std::make_unique<PrimitiveConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), predicate, pos)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_some_concept(const std::shared_ptr<const Role>& role, const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_concept_cache->insert(std::make_unique<SomeConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), role, concept)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_subset_concept(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_concept_cache->insert(std::make_unique<SubsetConcept>(m_vocabulary_info, m_caches.m_concept_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Concept> SyntacticElementFactoryImpl::make_top_concept() {
    return m_caches.m_concept_cache->insert(std::make_unique<TopConcept>(m_vocabulary_info, m_caches.m_concept_cache->size())).first;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::make_concept_distance_numerical(const std::shared_ptr<const Concept>& concept_from, const std::shared_ptr<const Role>& role, const std::shared_ptr<const Concept>& concept_to) {
    return m_caches.m_numerical_cache->insert(std::make_unique<ConceptDistanceNumerical>(m_vocabulary_info, m_caches.m_numerical_cache->size(), concept_from, role, concept_to)).first;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::make_count_numerical(const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_numerical_cache->insert(std::make_unique<CountNumerical<Concept>>(m_vocabulary_info, m_caches.m_numerical_cache->size(), concept)).first;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::make_count_numerical(const std::shared_ptr<const Role>& role) {
    return m_caches.m_numerical_cache->insert(std::make_unique<CountNumerical<Role>>(m_vocabulary_info, m_caches.m_numerical_cache->size(), role)).first;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::make_role_distance_numerical(const std::shared_ptr<const Role>& role_from, const std::shared_ptr<const Role>& role, const std::shared_ptr<const Role>& role_to) {
    return m_caches.m_numerical_cache->insert(std::make_unique<RoleDistanceNumerical>(m_vocabulary_info, m_caches.m_numerical_cache->size(), role_from, role, role_to)).first;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::make_sum_concept_distance_numerical(const std::shared_ptr<const Concept>& concept_from, const std::shared_ptr<const Role>& role, const std::shared_ptr<const Concept>& concept_to) {
    return m_caches.m_numerical_cache->insert(std::make_unique<SumConceptDistanceNumerical>(m_vocabulary_info, m_caches.m_numerical_cache->size(), concept_from, role, concept_to)).first;
}

std::shared_ptr<const Numerical> SyntacticElementFactoryImpl::make_sum_role_distance_numerical(const std::shared_ptr<const Role>& role_from, const std::shared_ptr<const Role>& role, const std::shared_ptr<const Role>& role_to) {
    return m_caches.m_numerical_cache->insert(std::make_unique<SumRoleDistanceNumerical>(m_vocabulary_info, m_caches.m_numerical_cache->size(), role_from, role, role_to)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_and_role(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_role_cache->insert(std::make_unique<AndRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_compose_role(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_role_cache->insert(std::make_unique<ComposeRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_diff_role(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_role_cache->insert(std::make_unique<DiffRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_identity_role(const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_role_cache->insert(std::make_unique<IdentityRole>(m_vocabulary_info, m_caches.m_role_cache->size(), concept)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_inverse_role(const std::shared_ptr<const Role>& role) {
    return m_caches.m_role_cache->insert(std::make_unique<InverseRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_not_role(const std::shared_ptr<const Role>& role) {
    return m_caches.m_role_cache->insert(std::make_unique<NotRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_or_role(const std::shared_ptr<const Role>& role_left, const std::shared_ptr<const Role>& role_right) {
    return m_caches.m_role_cache->insert(std::make_unique<OrRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role_left, role_right)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_primitive_role(const Predicate& predicate, int pos_1, int pos_2) {
    return m_caches.m_role_cache->insert(std::make_unique<PrimitiveRole>(m_vocabulary_info, m_caches.m_role_cache->size(), predicate, pos_1, pos_2)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_restrict_role(const std::shared_ptr<const Role>& role, const std::shared_ptr<const Concept>& concept) {
    return m_caches.m_role_cache->insert(std::make_unique<RestrictRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role, concept)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_top_role() {
    return m_caches.m_role_cache->insert(std::make_unique<TopRole>(m_vocabulary_info, m_caches.m_role_cache->size())).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_transitive_closure(const std::shared_ptr<const Role>& role) {
    return m_caches.m_role_cache->insert(std::make_unique<TransitiveClosureRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role)).first;
}

std::shared_ptr<const Role> SyntacticElementFactoryImpl::make_transitive_reflexive_closure(const std::shared_ptr<const Role>& role) {
    return m_caches.m_role_cache->insert(std::make_unique<TransitiveReflexiveClosureRole>(m_vocabulary_info, m_caches.m_role_cache->size(), role)).first;
}

std::shared_ptr<VocabularyInfo> SyntacticElementFactoryImpl::get_vocabulary_info() const {
    return m_vocabulary_info;
}

}


namespace boost::serialization {
template<typename Archive>
void serialize(Archive& ar, dlplan::core::SyntacticElementFactoryImpl& t, const unsigned int /* version */ )
{
    ar & t.m_vocabulary_info;
    ar & t.m_caches;
}

template void serialize(boost::archive::text_iarchive& ar,
    dlplan::core::SyntacticElementFactoryImpl& t, const unsigned int version);
template void serialize(boost::archive::text_oarchive& ar,
    dlplan::core::SyntacticElementFactoryImpl& t, const unsigned int version);
}
