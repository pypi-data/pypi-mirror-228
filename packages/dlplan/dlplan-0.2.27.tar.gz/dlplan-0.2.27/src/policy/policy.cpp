#include "../include/dlplan/policy.h"

#include <iostream>

#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>

#include "condition.h"
#include "effect.h"
#include "policy_builder.h"
#include "reader.h"
#include "writer.h"
#include "../../include/dlplan/policy.h"


namespace dlplan::policy {


BaseCondition::BaseCondition(ConditionIndex index) : m_index(index) { }

BaseCondition::~BaseCondition() = default;

ConditionIndex BaseCondition::get_index() const {
    return m_index;
}


BaseEffect::BaseEffect(EffectIndex index) : m_index(index) { }

BaseEffect::~BaseEffect() = default;

EffectIndex BaseEffect::get_index() const {
    return m_index;
}


PolicyBuilder::PolicyBuilder() = default;

PolicyBuilder::PolicyBuilder(const PolicyBuilder& other)
    : m_pImpl(*other.m_pImpl) { }

PolicyBuilder& PolicyBuilder::operator=(const PolicyBuilder& other) {
    if (this != &other) {
        *m_pImpl = *other.m_pImpl;
    }
    return *this;
}

PolicyBuilder::PolicyBuilder(PolicyBuilder&& other)
    : m_pImpl(std::move(*other.m_pImpl)) { }

PolicyBuilder& PolicyBuilder::operator=(PolicyBuilder&& other) {
    if (this != &other) {
        std::swap(*m_pImpl, *other.m_pImpl);
    }
    return *this;
}

PolicyBuilder::~PolicyBuilder() = default;

std::shared_ptr<const BaseCondition> PolicyBuilder::add_pos_condition(const std::shared_ptr<const core::Boolean>& boolean) {
    return m_pImpl->add_pos_condition(boolean);
}

std::shared_ptr<const BaseCondition> PolicyBuilder::add_neg_condition(const std::shared_ptr<const core::Boolean>& boolean) {
    return m_pImpl->add_neg_condition(boolean);
}

std::shared_ptr<const BaseCondition> PolicyBuilder::add_gt_condition(const std::shared_ptr<const core::Numerical>& numerical) {
    return m_pImpl->add_gt_condition(numerical);
}

std::shared_ptr<const BaseCondition> PolicyBuilder::add_eq_condition(const std::shared_ptr<const core::Numerical>& numerical) {
    return m_pImpl->add_eq_condition(numerical);
}

std::shared_ptr<const BaseEffect> PolicyBuilder::add_pos_effect(const std::shared_ptr<const core::Boolean>& boolean) {
    return m_pImpl->add_pos_effect(boolean);
}

std::shared_ptr<const BaseEffect> PolicyBuilder::add_neg_effect(const std::shared_ptr<const core::Boolean>& boolean) {
    return m_pImpl->add_neg_effect(boolean);
}

std::shared_ptr<const BaseEffect> PolicyBuilder::add_bot_effect(const std::shared_ptr<const core::Boolean>& boolean) {
    return m_pImpl->add_bot_effect(boolean);
}

std::shared_ptr<const BaseEffect> PolicyBuilder::add_inc_effect(const std::shared_ptr<const core::Numerical>& numerical) {
    return m_pImpl->add_inc_effect(numerical);
}

std::shared_ptr<const BaseEffect> PolicyBuilder::add_dec_effect(const std::shared_ptr<const core::Numerical>& numerical) {
    return m_pImpl->add_dec_effect(numerical);
}

std::shared_ptr<const BaseEffect> PolicyBuilder::add_bot_effect(const std::shared_ptr<const core::Numerical>& numerical) {
    return m_pImpl->add_bot_effect(numerical);
}

std::shared_ptr<const Rule> PolicyBuilder::add_rule(
    Conditions&& conditions,
    Effects&& effects) {
    return m_pImpl->add_rule(std::move(conditions), std::move(effects));
}

std::shared_ptr<const Policy> PolicyBuilder::add_policy(
    Rules&& rules) {
    return m_pImpl->add_policy(std::move(rules));
}


PolicyReader::PolicyReader() = default;

PolicyReader::PolicyReader(const PolicyReader& other)
    : m_pImpl(*other.m_pImpl) { }

PolicyReader& PolicyReader::operator=(const PolicyReader& other) {
    if (this != &other) {
        *m_pImpl = *other.m_pImpl;
    }
    return *this;
}

PolicyReader::PolicyReader(PolicyReader&& other)
    : m_pImpl(std::move(*other.m_pImpl)) { }

PolicyReader& PolicyReader::operator=(PolicyReader&& other) {
    if (this != &other) {
        std::swap(*m_pImpl, *other.m_pImpl);
    }
    return *this;
}

PolicyReader::~PolicyReader() = default;

std::shared_ptr<const Policy> PolicyReader::read(const std::string& data, PolicyBuilder& builder, core::SyntacticElementFactory& factory) const {
    return m_pImpl->read(data, builder, factory);
}


PolicyWriter::PolicyWriter() { }

PolicyWriter::PolicyWriter(const PolicyWriter& other)
    : m_pImpl(*other.m_pImpl) { }

PolicyWriter& PolicyWriter::operator=(const PolicyWriter& other) {
    if (this != &other) {
        *m_pImpl = *other.m_pImpl;
    }
    return *this;
}

PolicyWriter::PolicyWriter(PolicyWriter&& other)
    : m_pImpl(std::move(*other.m_pImpl)) { }

PolicyWriter& PolicyWriter::operator=(PolicyWriter&& other) {
    if (this != &other) {
        std::swap(*m_pImpl, *other.m_pImpl);
    }
    return *this;
}

PolicyWriter::~PolicyWriter() { }

std::string PolicyWriter::write(const Policy& policy) const {
    return m_pImpl->write(policy);
}

}


namespace boost::serialization {
template<typename Archive>
void serialize( Archive& /* ar */ , dlplan::policy::BaseCondition& /* t */ , const unsigned int /* version */ )
{
}

template<class Archive>
void save_construct_data(Archive& /* ar */ , const dlplan::policy::BaseCondition* /* t */ , const unsigned int /* version */ )
{
}

template<class Archive>
void load_construct_data(Archive& /* ar */ , dlplan::policy::BaseCondition* /* t */ , const unsigned int /* version */ )
{
}

template<typename Archive>
void serialize( Archive& /* ar */ , dlplan::policy::BaseEffect& /* t */ , const unsigned int /* version */ )
{
}

template<class Archive>
void save_construct_data(Archive& /* ar */ , const dlplan::policy::BaseEffect* /* t */ , const unsigned int /* version */ )
{
}

template<class Archive>
void load_construct_data(Archive& /* ar */ , dlplan::policy::BaseEffect* /* t */ , const unsigned int /* version */ )
{
}

template<typename Archive>
void serialize( Archive& ar, dlplan::policy::PolicyBuilder& t, const unsigned int /* version */ )
{
    ar & t.m_pImpl;
}

template void serialize(boost::archive::text_iarchive& ar,
    dlplan::policy::BaseCondition& t, const unsigned int version);
template void serialize(boost::archive::text_oarchive& ar,
    dlplan::policy::BaseCondition& t, const unsigned int version);
template void save_construct_data(boost::archive::text_oarchive& ar,
    const dlplan::policy::BaseCondition* t, const unsigned int version);
template void load_construct_data(boost::archive::text_iarchive& ar,
    dlplan::policy::BaseCondition* t, const unsigned int version);

template void serialize(boost::archive::text_iarchive& ar,
    dlplan::policy::BaseEffect& t, const unsigned int version);
template void serialize(boost::archive::text_oarchive& ar,
    dlplan::policy::BaseEffect& t, const unsigned int version);
template void save_construct_data(boost::archive::text_oarchive& ar,
    const dlplan::policy::BaseEffect* t, const unsigned int version);
template void load_construct_data(boost::archive::text_iarchive& ar,
    dlplan::policy::BaseEffect* t, const unsigned int version);

template void serialize(boost::archive::text_iarchive& ar,
    dlplan::policy::PolicyBuilder& t, const unsigned int version);
template void serialize(boost::archive::text_oarchive& ar,
    dlplan::policy::PolicyBuilder& t, const unsigned int version);
}
