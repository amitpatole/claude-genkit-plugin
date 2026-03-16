import pytest
from backend.tickerpulse.genkit_flow import get_flow_template, create_flow_template, update_flow_template, delete_flow_template
from backend.tickerpulse import db
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_flow_template():
    async with AsyncSession(db.engine) as session:
        await session.delete(await get_flow_template('test_template'))
        await session.commit()
        await create_flow_template('test_template', {'steps': ['step1', 'step2']})
        assert await get_flow_template('test_template') == {'steps': ['step1', 'step2']}

@pytest.mark.asyncio
async def test_update_flow_template():
    async with AsyncSession(db.engine) as session:
        await session.delete(await get_flow_template('test_template'))
        await session.commit()
        await create_flow_template('test_template', {'steps': ['step1', 'step2']})
        await update_flow_template('test_template', {'steps': ['step1', 'step2', 'step3']})
        assert await get_flow_template('test_template') == {'steps': ['step1', 'step2', 'step3']}

@pytest.mark.asyncio
async def test_delete_flow_template():
    async with AsyncSession(db.engine) as session:
        await session.delete(await get_flow_template('test_template'))
        await session.commit()
        await create_flow_template('test_template', {'steps': ['step1', 'step2']})
        await delete_flow_template('test_template')
        assert await get_flow_template('test_template') is None

@pytest.mark.asyncio
async def test_stream_flow_templates():
    async with AsyncSession(db.engine) as session:
        await session.delete(await get_flow_template('test_template'))
        await session.commit()
        await create_flow_template('test_template', {'steps': ['step1', 'step2']})
        templates = [template async for template in stream_flow_templates()]
        assert templates == [{'name': 'test_template', 'template': {'steps': ['step1', 'step2']}}]